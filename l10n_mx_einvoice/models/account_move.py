# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from xml.dom.minidom import parseString
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    """
    @api.model_cr
    def init(self):
        cr = self._cr
        cr.execute("delete from ir_ui_view where name='report_invoice_document_inherit_sale';")
    """
    
    @api.depends('journal_id')
    def _get_address_issued_invoice(self):
        for rec in self:
            rec.address_issued_id = rec.journal_id.address_invoice_company_id or \
                                    (rec.journal_id.company2_id and rec.journal_id.company2_id.partner_id) or \
                                    rec.journal_id.company_id.partner_id or False
            rec.company_emitter_id = rec.journal_id.company2_id or rec.journal_id.company_id or False

    def _get_xml_file_content(self):
        attachment = self.env['ir.attachment'].search([('res_model', '=', 'account.move'), ('res_id', '=', self.id), ('name', 'ilike', '.xml')], limit=1)
        if not attachment:
            return False
        try:
            file_path = self.env['ir.attachment']._full_path('checklist').replace('checklist','') + attachment.store_fname
            attach_file = open(file_path, 'rb')
            xml_data = attach_file.read()
            attach_file.close()
            return xml_data
        except:
            _logger.error("No se pudo leer el archivo XML adjunto a esta factura, favor de revisar...")
            return False
        
        
    
    @api.depends('cfdi_state','ref','state')
    def _get_uuid_from_attachment(self):
        for rec in self:
            rec.sat_serie = False
            rec.sat_uuid = False
            rec.sat_folio = False
            xml_data = rec._get_xml_file_content()
            if xml_data:
                #try:
                arch_xml = parseString(xml_data)
                is_xml_signed = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')
                if is_xml_signed:
                    xvalue = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
                    yvalue = arch_xml.getElementsByTagName('cfdi:Comprobante')[0]                    
                    timbre = xvalue.attributes['UUID'].value
                    serie, folio = False, False
                    try:
                        serie = yvalue.attributes['serie'].value
                    except:
                        pass
                    try:
                        folio = yvalue.attributes['folio'].value
                    except:
                        pass
                    res = self.search([('sat_uuid', '=', timbre),('id','!=',rec.id),('company_id','=',rec.company_id.id)])
                    if res:
                        raise UserError(_("Error ! La factura ya se encuentra registrada en el sistema y no puede tener registro duplicado.\n\nLa factura con Folio Fiscal %s se encuentra registrada en el registro %s - Referencia: %s - ID: %s")%(timbre, res.name, res.ref, res.id))
                    rec.sat_uuid = timbre
                    if serie:
                        rec.sat_serie = serie
                    if folio:
                        rec.sat_folio = folio
                    _logger.info("CFDI (Archivo XML) con UUID %s procesado exitosamente..." % timbre)
                    #except:
                    #    _logger.info("Ocurrió un error al intentar tomar los datos del archivo XML")
                    #    pass


    
    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state')
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for rec in self.filtered(lambda w: w.is_invoice(include_receipts=True)):
            rec.amount_discount = sum(line.amount_discount for line in self.invoice_line_ids) or 0.0
            rec.amount_subtotal = sum(line.amount_subtotal for line in self.invoice_line_ids) or 0.0
    
    
    @api.depends('amount_total','currency_id')
    def _get_amount_to_text(self):
        for rec in self:
            currency = rec.currency_id.name.upper()
            # M.N. = Moneda Nacional (National Currency)
            # M.E. = Moneda Extranjera (Foreign Currency)
            currency_type = 'M.N.' if currency == 'MXN' else 'M.E.'
            # Split integer and decimal part
            amount_i, amount_d = divmod(rec.amount_total, 1)
            amount_d = round(amount_d, 2)
            amount_d = int(amount_d * 100)
            words = rec.company_id.currency_id.with_context(lang=self.env.user.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
            invoice_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
                words=words, amount_d=amount_d, curr_t=currency_type)
            if currency != 'MXN':
                invoice_words = invoice_words.replace('PESOS',currency)
                invoice_words = invoice_words.replace('M.N.','M.E.')
            rec.amount_to_text = invoice_words
    
    
    @api.depends('invoice_line_ids.product_id')
    def _compute_deposit_invoice(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        deposit_product_id_setting =  int(ICPSudo.get_param('sale.default_deposit_product_id','0'))
        for rec in self:
            if deposit_product_id_setting and rec.invoice_line_ids:
                rec.deposit_invoice = bool(any(l.product_id.id == deposit_product_id_setting for l in rec.invoice_line_ids))
            else:
                rec.deposit_invoice = False
    
    @api.depends('cfdi_state','state','cancelation_request_ids')
    def _get_state_cancelation_requests(self):
        for rec in self:
            if not rec.cancelation_request_ids:
                rec.mailbox_state = "no"
            else:
                last_request = rec.cancelation_request_ids[-1]
                rec.mailbox_state = last_request.state
    
    use_for_cfdi = fields.Boolean(string="Usar para CFDIs", related="journal_id.use_for_cfdi")
    uso_cfdi_id = fields.Many2one('sat.uso.cfdi', 'Uso CFDI', readonly=True, 
                                  states={'draft': [('readonly', False)]},
                                  required=False) 
    type_document_id = fields.Many2one('sat.tipo.comprobante', 'Tipo de Comprobante', required=False) 
    metodo_pago_id = fields.Many2one('sat.metodo.pago','Metodo de Pago', readonly=True, 
                                      states={'draft': [('readonly', False)]},
                                     help='Metodo de Pago Requerido por el SAT')
    type_rel_cfdi_ids = fields.One2many('sat.invoice.cfdi.rel', 'invoice_rel_id', 'CFDI Relacionados') 
    tipo_cambio = fields.Float('Tipo Cambio', digits=(14,6), default=1.0)
    type_rel_id = fields.Many2one('sat.tipo.relacion.cfdi','Relacion CFDI',
                                 readonly=True, states={'draft': [('readonly', False)]})

    deposit_invoice = fields.Boolean('Anticipo', compute='_compute_deposit_invoice', store=True)

    deposit_invoice_used = fields.Boolean('Anticipo Relacionado', help='Indica que esta factura ya fue relacionada en el XML de otra.', copy=False )

    deposit_invoice_rel_id = fields.Many2one('account.move','Factura Relacionada como Anticipo', help='Indica a que factura fue relacionada en su XML.', copy=False )
    cfdi_complemento = fields.Selection([('na','No Aplica')], string='Complemento CFDI', 
                                        readonly=True, states={'draft': [('readonly', False)]}, 
                                        copy=False, store=True, default=lambda a:'na', required=True)

    
    amount_discount = fields.Monetary(string='Total Descuento', store=True, 
                                      readonly=True, compute='_compute_amount',
                                      tracking=True)
    amount_subtotal = fields.Monetary(string='Total Subtotal', store=True, readonly=True, compute='_compute_amount')
    
    sat_uuid = fields.Char(compute='_get_uuid_from_attachment', string="CFDI UUID", required=False, store=True, index=True)
    sat_folio = fields.Char(compute='_get_uuid_from_attachment', string="CFDI Folio", required=False, store=True, index=True)
    sat_serie = fields.Char(compute='_get_uuid_from_attachment', string="CFDI Serie", required=False, store=True, index=True)
    
    #### Columns ###################

    fname_invoice   =  fields.Char(compute='_get_fname_invoice', string='Nombre de Archivo',
                                    help='Nombre usado para el archivo XML del CFDI')
    invoice_datetime = fields.Datetime(string='Fecha CFDI', readonly=True, 
                                       states={'draft': [('readonly', False)]}, copy=False,
                                      help="Deje vacío para usar la fecha actual")
    date_invoice_tz = fields.Datetime(string='Fecha Factura con TZ', compute='_get_date_invoice_tz',
                                     help='Fecha de la Factura con Zona Horaria', copy=False)
    amount_to_text  = fields.Char(compute='_get_amount_to_text', string='Monto en texto', store=True,
                                  help='Monto de la Factura en texto')
    # Campos donde se guardara la info de CFDI
    
    no_certificado  = fields.Char(string='No. Certificado', size=64, help='Number of serie of certificate used for the invoice')
    certificado     = fields.Text('Certificado', help='Certificate used in the invoice')
    sello           = fields.Text('Sello', help='Digital Stamp')
    cadena_original = fields.Text('Cadena Original.')
        
    
    
    cfdi_cbb               = fields.Binary(string='Código Bidimensional', readonly=True, copy=False)
    cfdi_sello             = fields.Text('CFDI Sello',  readonly=True, help='Sign assigned by the SAT', copy=False)
    cfdi_no_certificado    = fields.Char('CFDI No. Certificado', size=32, readonly=True,
                                       help='Serial Number of the Certificate', copy=False)
    cfdi_cadena_original   = fields.Text(string='Cadena Original', readonly=True, copy=False)
    cfdi_fecha_timbrado    = fields.Datetime(string='Fecha Timbrado', readonly=True, copy=False)
    cfdi_fecha_cancelacion = fields.Datetime(string='Fecha Cancelación', readonly=True,
                                             help='Fecha cuando la factura es Cancelada', copy=False)
    cfdi_folio_fiscal      = fields.Char(string='Folio Fiscal (UUID)', size=64, readonly=True,
                                         help='Folio Fiscal del Comprobante CFDI, también llamado UUID', copy=False)

    cfdi_state             = fields.Selection([('draft','Pendiente'),
                                               ('xml_unsigned','XML a Timbrar'),
                                               ('xml_signed','XML Timbrado'),
                                               ('pdf','PDF del CFDI'),
                                               ('sent', 'CFDI Enviado por Correo'),
                                               ('in_process_cancel','CFDI En proceso cancelación'),
                                               ('uuid_no_cancel','CFDI no Cancelable'),
                                               ('uuid_no_cancel_by_customer','CFDI no Cancelable por el Cliente'),
                                               ('cancel','Cancelado'),
                                               ], string="Estado CFDI", readonly=True, default='draft',
                                     help='Estado del Proceso para generar el Comprobante Fiscal', copy=False)
    
    
    cancelation_request_ids = fields.One2many('account.move.cancelation.record', 'invoice_id', 'Solicitudes de Cancelación', copy=False)
    mailbox_state = fields.Selection([('cancel','Cancelacion Solicitud'),
                                      ('no','Sin Solicitudes'),
                                      ('process','En Proceso'),
                                      ('done','Aceptada'),
                                      ('rejected','Rechazada por el Cliente'),
                                      ('no_cancel','CFDI no se puede Cancelar')], 
                                     string='Estado Cancelacion', compute="_get_state_cancelation_requests", 
                                     store=True, tracking=True)
    cancel_wht_mailbox = fields.Boolean('Cancelar sin Solicitud', copy=False, tracking=True)
        
    # PENDIENTE => Definir el metodo donde se usaran
    #pdf_file_signed         = fields.Binary(string='Archivo PDF Timbrado', readonly=True, help='Archivo XML que se manda a Timbrar al PAC', copy=False)
    #xml_file_no_sign        = fields.Binary(string='Archivo XML a Timbrar', readonly=True, help='Archivo XML que se manda a Timbrar al PAC', copy=False)
    #xml_file_signed         = fields.Binary(string='Archivo XML Timbrado', readonly=True, help='Archivo XML final (después de timbrado y Addendas)', copy=False)
    xml_file_no_sign_index  = fields.Text(string='XML a Timbrar', readonly=True, help='Contenido del Archivo XML que se manda a Timbrar al PAC', copy=False)
    xml_file_signed_index   = fields.Text(string='XML Timbrado', readonly=True, help='Contenido del Archivo XML final (después de timbrado y Addendas)', copy=False)
    cfdi_last_message       = fields.Text(string='Last Message', readonly=True, help='Message generated to upload XML to sign', copy=False)
    xml_acuse_cancelacion   = fields.Text('XML Acuse Cancelacion', readonly=True)
    cfdi_pac                = fields.Selection([], string='PAC', readonly=True, store=True, copy=False)
    #pac_id                  = fields.Many2one('params.pac', string='Pac', readonly=True, help='Pac usado para Timbrar la Factura')
    
    ##################################
    pay_method_id   = fields.Many2one('pay.method', string='Forma de Pago', readonly=True, 
                                      states={'draft': [('readonly', False)]})
    
    pay_method_ids  = fields.Many2many('pay.method', 'account_invoice_pay_method_rel', 'invoice_id', 'pay_method_id', 
                                       readonly=True, states={'draft': [('readonly', False)]},
                                       string="Formas de Pago")
    
    acc_payment     = fields.Many2one('res.partner.bank', string='Cuenta Bancaria', readonly=True, 
                                      states={'draft': [('readonly', False)]},
            help='Is the account with which the client pays the invoice, \
            if not know which account will used for pay leave empty and \
            the XML will show "“Unidentified”".')


    address_issued_id = fields.Many2one('res.partner', compute='_get_address_issued_invoice', 
                                        string='Dirección Emisión', store=True,
                                        help='This address will be used as address that issued for electronic invoice')
    
    company_emitter_id = fields.Many2one('res.company', compute='_get_address_issued_invoice', store=True,
                                         string='Compañía Emisora', 
                                         help='This company will be used as emitter company in the electronic invoice')
                                         

    ## DESMARCAR COMENTARIO payment_line_ids = fields.One2many('account.payment.invoice', 'invoice_id', 'Pagos', readonly=True)
    l10n_mx_edi_is_required = fields.Boolean(string="Dummy", 
                                             help="Este campo es dummy porque lo usa el modulo l10n_mx_edi y afecta en el Template del envio de factura ")
    
    
    
    @api.depends('number', 'journal_id', 'invoice_date')
    def name_get(self):
        result = []
        for rec in self:
            if rec.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund'):
                if rec.name and rec.journal_id and rec.invoice_date:
                    name = rec.name + ' / ' + rec.journal_id.name + ' / ' + rec.invoice_date.isoformat()  
                    result.append((rec.id, name))
                else:
                    if rec.invoice_date:
                        name = 'SN' + ' / ' + rec.journal_id.name + ' / ' + rec.invoice_date.isoformat()
                    else:
                        name = 'SN' + ' / ' + rec.journal_id.name 
                    result.append((rec.id, name))
            else:
                result.append((rec.id, rec.name))
        return result


    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self.metodo_pago_id = self.partner_id.commercial_partner_id.property_payment_term_id.id
        self.uso_cfdi_id = self.partner_id.commercial_partner_id.uso_cfdi_id.id
        self.pay_method_id = self.partner_id.commercial_partner_id.pay_method_id.id
        return res
    
    
    @api.onchange('invoice_payment_term_id')
    def _invoice_payment_term_id(self):
        if self.invoice_payment_term_id:
            self.metodo_pago_id = self.invoice_payment_term_id.metodo_pago_id.id
        else:
            self.metodo_pago_id = False

    """
    def post(self):
        sat_tipo_obj = self.env['sat.tipo.comprobante']
        for rec in self.filtered(lambda w: w.is_invoice(include_receipts=True) and \
                                           w.type in ('out_invoice','out_refund') and \
                                           w.journal_id.use_for_cfdi):
            if not rec.uso_cfdi_id:
                raise UserError('Error!\nEl campo Uso CFDI es Obligatorio.')
            tipo_documento = 'I' if rec.type == 'out_invoice' else 'E'
            tipo_id = sat_tipo_obj.search([('code','=',tipo_documento)], limit=1)
            rec.type_document_id = tipo_id.id if tipo_id else False
        res = super(AccountMove, self).post()
        return res
    """

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        sat_tipo_obj = self.env['sat.tipo.comprobante']
        type_document = res.move_type
        tipo_documento = 'I' if res.move_type == 'out_invoice' else 'E'
        tipo_id = sat_tipo_obj.search([('code','=',tipo_documento)], limit=1)
        res.type_document_id = tipo_id.id if tipo_id else False
        if res.move_type == 'out_invoice':
            if not res.metodo_pago_id:
                if res.invoice_payment_term_id and res.invoice_payment_term_id.metodo_pago_id:
                    res.metodo_pago_id = res.invoice_payment_term_id.metodo_pago_id.id
                else:
                    metodo_pago_id = self.env.ref('l10n_mx_einvoice.metodo_00', False)
                    if metodo_pago_id:
                        res.metodo_pago_id = metodo_pago_id.id
            if not res.uso_cfdi_id:
                if res.partner_id and res.partner_id.uso_cfdi_id:
                    res.uso_cfdi_id = res.partner_id.uso_cfdi_id.id
                else:
                    uso_cfdi_id = self.env.ref('l10n_mx_einvoice.sat_usdo_cfdi_03', False)
                    if uso_cfdi_id:
                        res.uso_cfdi_id = uso_cfdi_id.id
            if not res.pay_method_id:
                if res.partner_id and res.partner_id.pay_method_id:
                    res.pay_method_id = res.partner_id.pay_method_id.id
                else:
                    pay_method_id = self.env.ref('l10n_mx_einvoice.pay_method_01', False)
                    if pay_method_id:
                        res.pay_method_id = pay_method_id.id

        return res

        

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    
    @api.depends('discount', 'price_unit', 'quantity')
    def _compute_discount_amounts(self):
        for line in self:
            line.amount_subtotal = line.price_unit * line.quantity
            line.amount_discount = (line.discount/100.0) * line.price_unit * line.quantity
        
    amount_discount = fields.Monetary(string='Monto Descuento', store=True, 
                                      compute='_compute_discount_amounts')
    amount_subtotal = fields.Monetary(string='Monto sin Descuento', store=True, 
                                      compute='_compute_discount_amounts')
    
    
    
class AccountPaymentTerm(models.Model):
    _inherit ='account.payment.term'

    metodo_pago_id = fields.Many2one('sat.metodo.pago','Metodo de Pago', 
                                     help='Metodo de Pago Requerido por el SAT', )


class SatInvoiceCFDIRel(models.Model):
    _name = 'sat.invoice.cfdi.rel'
    _description = 'Relacion de CFDI'
    #_rec_name = 'invoice_id' 

    payment_state = {
        'not_paid': 'No Pagada',
        'in_payment': 'En Proceso de Pago',
        'paid': 'Pagada',
        'partial': 'Parcialmente Pagada',
        'reversed': 'Reversada',
        'invoicing_legacy': 'Historico'}
    
    @api.depends('invoice_id')
    def _get_name_invoice_id(self):
        payment_state = {
        'not_paid': 'No Pagada',
        'in_payment': 'En Proceso de Pago',
        'paid': 'Pagada',
        'partial': 'Parcialmente Pagada',
        'reversed': 'Reversada',
        'invoicing_legacy': 'Historico'}
        for rec in self:
            _logger.info("")
            rec.name = '%s - %s - %s - %s' % (rec.invoice_id.name, rec.invoice_id.invoice_date, rec.invoice_id.cfdi_folio_fiscal, payment_state[rec.invoice_id.payment_state])
    
    name = fields.Char(string="Referencia",
                      compute="_get_name_invoice_id")
    invoice_id  = fields.Many2one('account.move', 'Factura', required=True)
    move_name   = fields.Char(string="Factura #", related="invoice_id.name")
    date_invoice= fields.Date(string="Fecha", related="invoice_id.invoice_date")
    cfdi_folio_fiscal = fields.Char(string="Folio Fiscal", related="invoice_id.cfdi_folio_fiscal")
    amount_total= fields.Monetary(string="Total", related="invoice_id.amount_total")
    currency_id = fields.Many2one('res.currency', string="Moneda", related="invoice_id.currency_id")
    payment_state = fields.Selection(string="Estado Pago", related="invoice_id.payment_state")
    state = fields.Selection(string='Estado', related="invoice_id.state")
                        
    invoice_rel_id = fields.Many2one('account.move', 'ID Rel')
    onchange_domain = fields.Boolean('Disparar Dominios', default=True)


    @api.onchange('onchange_domain')
    def onchange_relation(self):

        domain={}
        if self.invoice_rel_id.type_rel_id:
            if self.invoice_rel_id.type_rel_id.code == '07':
                domain.update({'invoice_id':[('deposit_invoice','=',True),
                                             ('deposit_invoice_used','=',False),
                                             ('payment_state','!=','not_paid'),
                                             ('move_type','in',('out_invoice','out_refund')),
                                             ('cfdi_folio_fiscal','!=',False)]
                              }) 
            elif self.invoice_rel_id.type_rel_id.code == '04':
                domain.update({'invoice_id':[('move_type','in',('out_invoice','out_refund')),
                                             ('cfdi_folio_fiscal','!=',False)]
                              })
            else:
                domain.update({'invoice_id':[('payment_state','!=','not_paid'),
                                             ('move_type','in',('out_invoice','out_refund')),
                                             ('cfdi_folio_fiscal','!=',False)]
                              }) 

        else:
            domain.update({'invoice_id':[('payment_state','!=','not_paid'),
                                         ('move_type','in',('out_invoice','out_refund')),
                                         ('cfdi_folio_fiscal','!=',False)]
                          })
        #print('domain: ', domain)
        return {'domain': domain}
    
    
class AccountMoveCancelationRecord(models.Model):
    _name = 'account.move.cancelation.record'
    _description = 'Solicitud de Cancelacion'
    _rec_name = 'folio_fiscal'     

    date_request = fields.Datetime('Fecha Solicitud', help='Indica la fecha en la que se realizo la Solicitud de Cancelacion', )
    state = fields.Selection([('cancel','Cancelacion Solicitud'),
                              ('process','En Proceso'),
                              ('done','Aceptada'),
                              ('rejected','Rechazada por el Cliente'),
                              ('no_cancel','CFDI no se puede Cancelar')], string='Estado Solicitud')
    invoice_id = fields.Many2one('account.move',string='ID Ref')
    request_ignored = fields.Boolean('Ignorar Solicitud')
    folio_fiscal = fields.Char('Folio Fiscal',size=128)
    message_invisible = fields.Text("Mensaje PAC")

    
    def solitud_cancelacion_asincrona(self):
        ## Se deja Abierta la Conexion para la Consulta con el PAC ###
        return {}

    
    
    def solitud_cancelacion_consulta_status(self):
        ## Se deja Abierta la Conexion para la Consulta con el PAC ###
        return {}
    
    
    def unlink_me(self):
        self.unlink()
