# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import operator
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta, time
import pytz

    

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
    
    
    user_id = fields.Many2one('res.users', string='Usuario', readonly=True, default=lambda self: self.env.user)
    num_operacion = fields.Char('Número de Operación', 
                                help="Indique número de cheque, número de autorización, número de referencia, "
                                     "clave de rastreo en caso de ser SPEI, línea de captura o algún número de referencia análogo que "
                                     "identifique la operación que ampara el pago efectuado (OPCIONAL)")
    
    pay_method_id   = fields.Many2one('pay.method', string='Forma de Pago', 
                                     help="Método de Pago. Recuerde que este Método de Pago es diferente al de Contabilidad Electrónica (Definido en el diario contable de Pago)")
    pay_method_id_code = fields.Char(related="pay_method_id.code", readonly=True)
    use_for_cfdi    = fields.Boolean(related="journal_id.use_for_cfdi", readonly=True)
    generar_cfdi    = fields.Boolean(string="Generar CFDI")
    payment_datetime_reception = fields.Datetime(string='Fecha Recepción de Pago')
    activar_relacion_cfdi = fields.Boolean(string="CFDI Relacionado",
                                           help="Permite relacionar CFDI de Pago por Tipo Relación con Clave 04 (Sustitución de los CFDIs Previos)")
    cfdi_relacionado_id = fields.Many2one('account.payment', string="CFDI Relacionado por sustitución",
                                          help="Aquí debe seleccionar el CFDI que quiere sustituir por este pago.")
    ### Datos Bancarios en XML  Ger ###
    no_data_bank_in_xml    = fields.Boolean(string="Sin Datos Bancarios", 
                                            help='No incluye los datos de Cuenta Ordenante y Beneficiaria dentro del XML.', )

    partner_id  = fields.Many2one('res.partner', string='Partner')
    # partner_parent_id = fields.Many2one('res.partner', related='partner_id.commercial_partner_id', string='Parent Partner')
    payment_type = fields.Selection([('outbound', 'Send Money'), 
                                     ('inbound', 'Receive Money')], 
                                    string='Payment Type', required=False, readonly=True)

    
    @api.model
    def default_get(self, fields):
        rec = super(AccountPaymentRegister, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        if not active_ids:
            return rec
        invoices = self.env['account.move'].browse(active_ids)
        payment_type = 'inbound' if invoices[0].move_type in ('out_invoice', 'in_refund', 'out_receipt') else 'outbound'
        partner_id = invoices[0].partner_id.id
        if payment_type == 'inbound':
            rec.update({'partner_id' : partner_id, 'payment_type' : payment_type })
            if any(inv.partner_id.id != partner_id for inv in invoices):
                raise UserError(_('Advertencia !!!\n Solo es posible registrar pagos de Clientes'))
        
        return rec
    
    
    @api.onchange('payment_date')
    def _onchange_payment_date(self):
        self._onchange_generar_cfdi()
    
    @api.onchange('generar_cfdi')
    def _onchange_generar_cfdi(self):
        if self.generar_cfdi:
            xdate = datetime.combine(self.payment_date, time(12,0))
            timezone = pytz.timezone(self.env.user.partner_id.tz or 'Mexico/General')
            xdate = timezone.localize(xdate)
            xdate = xdate.astimezone(pytz.timezone('UTC'))
            xdate = xdate.replace(tzinfo=None)
            self.payment_datetime_reception = xdate
        else:
            self.pay_method_id = False
            self.payment_datetime_reception = False
            self.num_operacion = False
            self.activar_relacion_cfdi = False

    
    @api.onchange('activar_relacion_cfdi')
    def _onchange_activar_relacion_cfdi(self):
        if not self.activar_relacion_cfdi:
            self.cfdi_relacionado_id = False
    
    def _create_payment_vals_from_wizard(self):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        _logger.info("res: %s" % res)
        res.update({
            'user_id'       : self.user_id.id,
            'num_operacion' : self.num_operacion,
            'pay_method_id' : self.pay_method_id.id,
            'generar_cfdi'  : self.generar_cfdi,
            'no_data_bank_in_xml'  : self.no_data_bank_in_xml,
            'payment_datetime_reception' : self.payment_datetime_reception,
            'activar_relacion_cfdi' : self.activar_relacion_cfdi,
            'cfdi_relacionado_id'   : self.cfdi_relacionado_id.id,
        })        
        return res

    
    def _create_payments(self):
        active_ids = self._context.get('active_ids')
        if not active_ids:
            return super(AccountPaymentRegister, self)._create_payments()
        # invoices = self.env['account.move'].browse(active_ids)
        # if self.generar_cfdi and len(invoices)==1:
        #     if invoices[0].metodo_pago_id and invoices[0].metodo_pago_id.code=='PUE':
        #         raise UserError(_("Error !!!\n\nEstá intentando crear un Recibo electronico de pagos "
        #                           "pero la Factura %s está definida como Pago en una sola exhibición") % (invoices[0].name))
        return super(AccountPaymentRegister, self)._create_payments()


    
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    @api.depends('cfdi_state','state')
    def _get_uuid_from_attachment(self):
        ir_attach_obj = self.env['ir.attachment']
        payment_obj = self.env['account.payment']
        for rec in self:
            rec.sat_uuid = False
            rec.sat_serie = False
            rec.sat_folio = False
            if rec.state not in ('draft','cancelled'):
                attachment_xml_ids = ir_attach_obj.search([('res_model', '=', 'account.payment'), 
                                                           ('res_id', '=', rec.id), 
                                                           ('name', 'ilike', '.xml')], limit=1)
                if attachment_xml_ids:
                    try:
                        xml_data = base64.b64decode(attachment_xml_ids.datas).replace('http://www.sat.gob.mx/cfd/3 ', '').replace('Rfc=','rfc=').replace('Fecha=','fecha=').replace('Total=','total=').replace('Folio=','folio=').replace('Serie=','serie=')
                        arch_xml = parseString(xml_data)
                        xvalue = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
                        timbre = xvalue.attributes['UUID'].value
                        serie, folio = False, False
                        try:
                            serie = xvalue.attributes['serie'].value
                        except:
                            pass
                        try:
                            folio = xvalue.attributes['folio'].value
                        except:
                            pass
                        res = payment_obj.search([('sat_uuid', '=', timbre),('id','!=',self.id)])
                        if res:
                            raise UserError(_("Error ! El pago ya se encuentra registrada en el sistema y no puede tener registro duplicado.\n\nEl Pago con Folio Fiscal %s se encuentra registrada en el registro %s - Referencia: %s - ID: %s")%(timbre, res.number, res.reference, res.id))
                        rec.sat_uuid = timbre
                        rec.sat_serie = serie
                        rec.sat_folio = folio
                    except:
                        pass    
    
    
    
    def _get_date_payment_tz(self):
        tz = self.env.user.partner_id.tz or 'America/Mexico_City'
        for rec in self:
            rec.date_payment_tz = rec.payment_datetime and self.server_to_local_timestamp(
                rec.payment_datetime, tz) or False
        rec.date_payment_reception_tz = rec.payment_datetime_reception and rec.server_to_local_timestamp(
                rec.payment_datetime_reception, tz) or False
    
    
    
    def _get_fname_payment(self):
        for rec in self:
            if not rec.journal_id.use_for_cfdi or (rec.payment_type != 'inbound' and rec.partner_type != 'customer'):
                rec.fname_payment = '.'
                return

            fname = rec.company_id.partner_id.vat + '_' + \
                    (rec.name and rec.name.replace('/','_').replace(' ','') or '')
            rec.fname_payment = fname 
        
        
    
    @api.depends('journal_id')
    def _get_address_issued_payment(self):
        for rec in self:
            rec.address_issued_id = rec.journal_id.address_invoice_company_id or \
                                    (rec.journal_id.company2_id and rec.journal_id.company2_id.address_invoice_parent_company_id) or \
                                    rec.journal_id.company_id.address_invoice_parent_company_id or False
            rec.company_emitter_id = rec.journal_id.company2_id or rec.journal_id.company_id or False

    
    def _get_date_2_cfdi_tz(self):
        for rec in self:
            dt_format = DEFAULT_SERVER_DATETIME_FORMAT        
            tz = self.env.user.partner_id.tz or 'America/Mexico_City'
            payment_datetime = str(datetime.now())[0:19]
            date_payment_tz = self.server_to_local_timestamp(
                    payment_datetime, tz) or False

            rec.date_2_cfdi_tz = date_payment_tz

    date_2_cfdi_tz = fields.Datetime(compute='_get_date_2_cfdi_tz',string='Fecha CFDI para timbrado', store=True, index=True)

    sat_uuid = fields.Char(compute='_get_uuid_from_attachment', string="CFDI UUID", required=False, store=True, index=True)
    sat_folio = fields.Char(compute='_get_uuid_from_attachment', string="CFDI Folio", required=False, store=True, index=True)
    sat_serie = fields.Char(compute='_get_uuid_from_attachment', string="CFDI Serie", required=False, store=True, index=True)
    
    user_id = fields.Many2one('res.users', string='Usuario', readonly=True, default=lambda self: self.env.user)
    uso_cfdi_id = fields.Many2one('sat.uso.cfdi', 'Uso CFDI', required=False, 
                                  default=lambda self: self.env['sat.uso.cfdi'].search([('code','=','P01')],limit=1)) 
    type_document_id = fields.Many2one('sat.tipo.comprobante', string='Tipo de Comprobante', required=False, 
                                       help='Define el motivo de la compra.', 
                                       default=lambda self: self.env['sat.tipo.comprobante'].search([('code','=','P')],limit=1)) 
    fname_payment   =  fields.Char(compute='_get_fname_payment', string='Nombre Archivo de Pago',
                                    help='Nombre del archivo a usar para los archivos XML y PDF del Pago')
    payment_datetime = fields.Datetime(string='Fecha Emisión CFDI', readonly=True, 
                                       states={'draft': [('readonly', False)]}, copy=False)
    payment_datetime_reception = fields.Datetime(string='Fecha Recepción Pago', copy=False)
    date_payment_tz = fields.Datetime(string='Fecha CFDI con TZ', compute='_get_date_payment_tz', copy=False)
    date_payment_reception_tz = fields.Datetime(string='Fecha Pago con TZ', compute='_get_date_payment_tz', copy=False)    
    amount_to_text  = fields.Char(compute='_get_amount_to_text', string='Amount to Text', store=True,
                                help='Amount of the invoice in letter')
    # Campos donde se guardara la info de CFDI    
    no_certificado  = fields.Char(string='No. Certificado', size=64, help='Number of serie of certificate used for the invoice')
    certificado     = fields.Text('Certificado', help='Certificate used in the invoice')
    sello           = fields.Text('Sello', help='Digital Stamp')
    cadena_original = fields.Text('Cadena Original', help='Data stream with the information contained in the electronic invoice') 
    
    cfdi_cbb               = fields.Binary(string='Imagen Código Bidimensional', readonly=True, copy=False)
    cfdi_sello             = fields.Text('CFDI Sello',  readonly=True, help='Sign assigned by the SAT', copy=False)
    cfdi_no_certificado    = fields.Char('CFDI No. Certificado', size=32, readonly=True,
                                       help='Serial Number of the Certificate', copy=False)
    cfdi_cadena_original   = fields.Text(string='CFDI Cadena Original', readonly=True,
                                        help='Original String used in the electronic invoice', copy=False)
    cfdi_fecha_timbrado    = fields.Datetime(string='Fecha Timbrado', readonly=True,
                                           help='Date when is stamped the electronic invoice', copy=False)
    cfdi_fecha_cancelacion = fields.Datetime(string='Fecha Cancelación', readonly=True,
                                             help='Fecha cuando la factura es Cancelada', copy=False)
    cfdi_folio_fiscal      = fields.Char(string='Folio Fiscal (UUID)', size=64, readonly=True,
                                     help='Folio Fiscal del Comprobante CFDI, también llamado UUID', copy=False)

    cfdi_state              = fields.Selection([('draft','Pendiente'),
                                                ('xml_unsigned','XML a Timbrar'),
                                                ('xml_signed','Timbrado'),
                                                ('pdf','PDF'),
                                                ('sent', 'Correo enviado'),
                                                ('cancel','Cancelado'),
                                                ], string="Estado CFDI", readonly=True, default='draft',
                                     help='Estado del Proceso para generar el Comprobante Fiscal', copy=False)
    
    
    # PENDIENTE => Definir el metodo donde se usaran
    xml_file_no_sign_index  = fields.Text(string='XML a Timbrar', readonly=True, help='Contenido del Archivo XML que se manda a Timbrar al PAC', copy=False)
    xml_file_signed_index   = fields.Text(string='XML Timbrado', readonly=True, help='Contenido del Archivo XML final (después de timbrado y Addendas)', copy=False)
    cfdi_last_message       = fields.Text(string='Last Message', readonly=True, help='Message generated to upload XML to sign', copy=False)
    xml_acuse_cancelacion   = fields.Text('XML Acuse Cancelacion', readonly=True)
    cfdi_pac                = fields.Selection([], string='PAC', readonly=True, store=True, copy=False)
    ##################################


    address_issued_id = fields.Many2one('res.partner', compute='_get_address_issued_payment', 
                                        string='Dirección Emisión', store=True,
                                        help='This address will be used as address that issued for electronic invoice')
    
    company_emitter_id = fields.Many2one('res.company', compute='_get_address_issued_payment', store=True,
                                         string='Compañía Emisora', 
                                         help='This company will be used as emitter company in the electronic invoice')
    
    

    payment_invoice_line_ids = fields.One2many('account.payment.invoice', 'payment_id', 'Desglose Facturas Pagadas', readonly=True)
    num_operacion = fields.Char('Número de Operación', 
                                help="Indique número de cheque, número de autorización, número de referencia, "
                                     "clave de rastreo en caso de ser SPEI, línea de captura o algún número de referencia análogo que "
                                     "identifique la operación que ampara el pago efectuado (OPCIONAL)")
    
    pay_method_id   = fields.Many2one('pay.method', string='Forma de Pago', readonly=True, 
                                      states={'draft': [('readonly', False)], 'posted': [('readonly', False)]},
                                     help="Método de Pago. Recuerde que este Método de Pago es diferente al de Contabilidad Electrónica (Definido en el diario contable de Pago)")
    
    pay_method_id_code = fields.Char(related="pay_method_id.code", readonly=True)
    use_for_cfdi    = fields.Boolean(related="journal_id.use_for_cfdi", readonly=True)
    generar_cfdi    = fields.Boolean(string="Generar CFDI")
    ### Datos Bancarios en XML  Ger ###
    no_data_bank_in_xml    = fields.Boolean(string="Sin Datos Bancarios", help='No incluye los datos de Cuenta Ordenante y Beneficiaria dentro del XML.', )
    ### FIN Ger ###
    tipo_cambio     = fields.Float('Tipo Cambio', digits=(14,6), default=1.0)
    activar_relacion_cfdi = fields.Boolean(string="CFDI Relacionado",
                                           help="Permite relacionar CFDI de Pago por Tipo Relación con Clave 04 (Sustitución de los CFDIs Previos)")
    cfdi_relacionado_id = fields.Many2one('account.payment', string="CFDI Relacionado por sustitución",
                                          help="Aquí debe seleccionar el CFDI que quiere sustituir por este pago.")
    
    comments = fields.Text("Comentarios")

    
    @api.onchange('date')
    def _onchange_payment_date(self):
        self._onchange_generar_cfdi()
    
    @api.onchange('generar_cfdi')
    def _onchange_generar_cfdi(self):
        if self.generar_cfdi:
            xdate = datetime.combine(self.date, time(12,0))
            timezone = pytz.timezone(self.env.user.partner_id.tz or 'Mexico/General')
            xdate = timezone.localize(xdate)
            xdate = xdate.astimezone(pytz.timezone('UTC'))
            xdate = xdate.replace(tzinfo=None)
            self.payment_datetime_reception = xdate
        else:
            self.pay_method_id = False
            self.payment_datetime_reception = False
            self.num_operacion = False
            self.activar_relacion_cfdi = False
    

    @api.onchange('activar_relacion_cfdi')
    def _onchange_activar_relacion_cfdi(self):
        if not self.activar_relacion_cfdi:
            self.cfdi_relacionado_id = False
            
    
    
    def get_driver_cfdi_sign(self):
        """function to inherit from module driver of pac and add particular function"""
        return {}

    
    def get_driver_cfdi_cancel(self):
        """function to inherit from module driver of pac and add particular function"""
        return {}
            
    def action_cancel(self):
        self.action_draft()
        res = super(AccountPayment, self).action_cancel()
        return res
    
class AccountPaymentInvoice(models.Model):
    _name = 'account.payment.invoice'
    _description="Parcialidades pagadas a facturas (para CFDI Pagos)"

    
    
    @api.depends('invoice_id', 'payment_id')
    def _get_currency_rate(self):
        for rec in self:
            if not rec.invoice_id or rec.invoice_id.currency_id == rec.env.user.company_id.currency_id:
                rec.invoice_currency_rate = 1.0
                return
            rec.invoice_currency_rate = round(1.0 / rec.invoice_id.currency_id.with_context({'date': rec.payment_date}).compute(1, rec.currency_id, round=False), 6)
        #if self.payment_currency_id == self.env.user.company_id.currency_id:
        #    self.invoice_currency_rate = abs(self.invoice_id.amount_total_signed / self.invoice_id.amount_total_company_signed)
        #else:
        #    self.invoice_currency_rate = abs(self.invoice_id.amount_total_company_signed / self.invoice_id.amount_total_signed)
     
    
    @api.depends('saldo_anterior', 'monto_pago')
    def _get_saldo_final(self):
        for rec in self:
            rec.saldo_final = round(rec.saldo_anterior - rec.monto_pago, 2)
        
    
    payment_id  = fields.Many2one('account.payment', 'Pago', required=True)
    payment_state = fields.Selection(string="Estado", readonly=True, related="payment_id.state")
    payment_currency_id = fields.Many2one('res.currency', string="Moneda de Pago", related='payment_id.currency_id', readonly=True)
    currency_id = fields.Many2one('res.currency', string="Moneda", related='payment_id.currency_id', readonly=True)
    payment_date = fields.Date(string="Fecha Pago", related='payment_id.date', readonly=True)
    payment_amount = fields.Monetary(string="Monto Pago", related='payment_id.amount', readonly=True)
    
    invoice_id  = fields.Many2one('account.move', string='Factura', required=True)
    invoice_serie = fields.Char(related='invoice_id.sat_serie', string='Serie', readonly=True)
    invoice_folio = fields.Char(related='invoice_id.sat_folio', string='Folio', readonly=True)
    invoice_uuid = fields.Char(related='invoice_id.sat_uuid', string='Folio Fiscal', readonly=True)
    invoice_currency_id = fields.Many2one('res.currency', string="Moneda Factura", related='invoice_id.currency_id', readonly=True)
    invoice_currency_rate = fields.Float(compute='_get_currency_rate', digits=(22, 16), readonly=True)
    
    parcialidad = fields.Integer('Parcialidad', default=1, required=True)
    saldo_anterior = fields.Float('Saldo Anterior', default=0.0, help="Saldo Anterior (en Moneda de la Factura)")
    monto_pago  = fields.Float('Monto Aplicado', default=0.0, help="Monto Pago (en Moneda de la Factura)")
    saldo_final = fields.Float('Saldo Insoluto', compute='_get_saldo_final', store=True,
                               help="Saldo Insoluto (en Moneda de la Factura) después del pago")
    
    
