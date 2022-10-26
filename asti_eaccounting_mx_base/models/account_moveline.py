# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree as et
from xml.dom.minidom import parse, parseString

import base64
import re
import logging
_logger = logging.getLogger(__name__)

_RFC_PATTERN = re.compile('[A-Z\xc3\x91&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z0-9]?[A-Z0-9]?[0-9A-Z]?')
_SERIES_PATTERN = re.compile('[A-Z]+')
_UUID_PATTERN = re.compile('[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}')

class eaccount_complement_types(models.Model):
    _name = 'eaccount.complement.types'
    _description = 'Tipos de Complementos de Contabilidad Electrónica'

    key  = fields.Char(string='Llave', size=20, required=True)
    name = fields.Char('Nombre', size=50, required=True)
    allowed_in_helper =  fields.Boolean(string='Helper exlusive', required=True)



class eaccount_complements(models.Model):
    _name = 'eaccount.complements'
    _description = 'Complementos para contabilidad electronica'
    
    move_line_id        = fields.Many2one('account.move.line', string='Partida', ondelete='cascade')
    move_id             = fields.Many2one('account.move', related='move_line_id.move_id', string='Póliza', readonly=True, store=True)
    file_data           = fields.Binary(string='Adjuntar')
    type_id             = fields.Many2one('eaccount.complement.types', string='Tipo ', default=lambda *a: False,
                                          help='Elija el tipo de complemento que desea anexar a la póliza.')
    type_key            = fields.Char(string='Type key', size=20)
    origin_bank_key     = fields.Char(string='Origin bank key', size=10)
    destiny_bank_key    = fields.Char(string='Destiny bank key', size=10)
    #show_native_accs    = fields.Boolean(string='Mostrar otras')
    #origin_account_id   = fields.Many2one('eaccount.bank.account', string='Cuenta origen')
    origin_account_id   = fields.Many2one('res.partner.bank', string='Cuenta origen')
    #origin_native_accid = fields.Many2one('res.partner.bank', string='Cuenta origen (otros)')
    payee_id            = fields.Many2one('res.partner', string='Beneficiario (Cliente / Proveedor)')
    payee_acc_id        = fields.Many2one('account.account', string='Beneficiario (Cta Contable)')
    #show_native_accs2   = fields.Boolean(string='Mostrar otras 2')
    #destiny_account_id  = fields.Many2one('eaccount.bank.account', string='Cuenta destino')
    destiny_account_id  = fields.Many2one('res.partner.bank', string='Cuenta destino')
    #destiny_native_accid= fields.Many2one('res.partner.bank', string='Cuenta destino (otros)')
    #show_native_accs1   = fields.Boolean(string='Mostrar otras 1')
    origin_bank_id      = fields.Many2one('res.bank', string='Banco nacional (origen)')
    origin_frgn_bank    = fields.Char(string='Banco extranjero (origen)', size=150)
    destiny_bank_id     = fields.Many2one('res.bank', string='Banco nacional (destino)')
    destiny_frgn_bank   = fields.Char(string='Banco extranjero (destino)', size=150)
    uuid                = fields.Char(string='UUId', size=36)
    amount              = fields.Float(string='Monto total')
    rfc                 = fields.Char(string='RFC Origen', size=13)
    rfc2                = fields.Char(string='RFC Destino', size=13)
    compl_date          = fields.Date(string='Fecha')
    pay_method_id       = fields.Many2one('eaccount.payment.methods', string='M\xc3\xa9todo de pago')
    compl_currency_id   = fields.Many2one('res.currency', string='Moneda', 
                                          default=lambda self: self.env.user.company_id.currency_id)
    exchange_rate       = fields.Float(string='Tipo de cambio', default=lambda *a: 1.0)
    cbb_series          = fields.Char(string='Serie', size=10)
    cbb_number          = fields.Integer(string='No. folio')
    foreign_invoice     = fields.Char(string='No. de factura extranjera', size=36)
    foreign_tax_id       = fields.Char(string='Contribuyente extranjero (Tax ID)', size=30)
    check_number        = fields.Char(string='No. Cheque', size=20)

    @api.onchange('type_id')
    def onchange_type(self):
        self.uuid = None
        self.cbb_series = None
        self.cbb_number = None
        self.foreign_invoice = None
        self.type_key = None
        self.origin_account_id = None
        #self.origin_native_accid = False
        #self.show_native_accs = False
        self.rfc = None
        self.origin_bank_id = None
        self.origin_frgn_bank = None
        self.destiny_account_id = None
        #self.destiny_native_accid = False
        #self.show_native_accs1 = False
        self.rfc2 = None
        self.destiny_bank_id = None
        self.destiny_frgn_bank = None
        self.payee_id = None
        self.payee_acc_id = None
        #self.show_native_accs2 = False
        self.foreign_tax_id = None
        self.check_number = None
        self.pay_method_id = None
        self.compl_currency_id = None
        self.exchange_rate = None
        if self.type_id:
            self.type_key = self.type_id.key
            has_rate_silent = 'rate_silent' in self.env.user.company_id.currency_id._fields.keys() or False
            if self.env.user.company_id.currency_id:
                """
                if self.type_id.key == 'check' and self.env.user.company_id.apply_in_check:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                elif self.type_id.key == 'transfer' and self.env.user.company_id.apply_in_trans:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                elif self.type_id.key == 'cfdi' and self.env.user.company_id.apply_in_cfdi:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                elif self.type_id.key == 'other' and self.env.user.company_id.apply_in_other:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                elif self.type_id.key == 'foreign' and self.env.user.company_id.apply_in_forgn:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                elif self.type_id.key == 'payment' and self.env.user.company_id.apply_in_paymth:
                    self.compl_currency_id = self.env.user.company_id.currency_id.id
                    self.exchange_rate = has_rate_silent and self.env.user.company_id.currency_id.rate_silent or self.env.user.company_id.currency_id.rate
                """
                if self.exchange_rate:
                    self.exchange_rate = 1 / self.exchange_rate

    """
    @api.onchange('bank_id')
    def onchange_bank(self):
        bkey = self.bank_id and bank.sat_bank_id.bic or False
        if self._context.get('is_origin', False):
            self.origin_bank_key = bkey
            self.origin_frgn_bank = (bkey == '999') and self.bank_id.name or False            
        else:
            self.destiny_bank_key = bkey
            self.destiny_frgn_bank = (bkey == '999') and self.bank_id.name or False
        #vals['origin_frgn_bank' if context.get('is_origin', False) else 'destiny_frgn_bank'] = bank.name if bkey == '999' else False
        #return {'value': vals}
    

        
    @api.onchange('origin_account_id')
    def onchange_origin_account_id(self):
        if self.origin_account_id:
            partner_rfc = self.origin_account_id.account_id.rfc
            self.origin_bank_id = self.origin_account_id.bank_id.id
            if partner_rfc:
                self.rfc = partner_rfc[2:] if len(partner_rfc) > 13 else partner_rfc
            if self._context.get('type_key', '') == 'transfer':
                self.payee_id = self.origin_account_id.account_id.id                
                self.show_native_accs2 = True
            else:
                self.payee_id = False
                self.show_native_accs2 = False
        else:
            self.rfc = False
            self.origin_bank_id = False
            self.payee_id = False
            self.show_native_accs2 = False
    """
            
    @api.onchange('origin_account_id')
    def onchange_origin_account_id(self):
        if self.origin_account_id:
            partner_rfc = self.origin_account_id.partner_id.vat
            self.origin_bank_id = self.origin_account_id.bank_id.id
            self.origin_bank_key = self.origin_account_id.bank_id.sat_bank_id.bic or False
            if partner_rfc:
                self.rfc = partner_rfc[2:] if len(partner_rfc) > 13 else partner_rfc
            #if self._context.get('type_key', '') == 'transfer':
            #    self.payee_id = self.origin_account_id.partner_id.id                
                ##self.show_native_accs2 = False
            #else:
                #self.payee_id = False
                ##self.show_native_accs2 = False
        else:
            self.rfc = False
            self.origin_bank_id = False
            self.payee_id = False
            self.origin_bank_key = False
            #self.show_native_accs2 = False            


    """
    @api.onchange('destiny_account_id')
    def onchange_destiny_account_id(self):
        if self.destiny_account_id:
            partner_rfc = self.destiny_account_id.account_id.rfc
            self.destiny_bank_id = self.destiny_account_id.bank_id.id
            if partner_rfc:
                self.rfc2 = partner_rfc[2:] if len(partner_rfc) > 13 else partner_rfc
            if self._context.get('type_key', '') == 'transfer':
                self.payee_acc_id = self.destiny_account_id.account_id.id                
                self.show_native_accs2 = True
            else:
                self.payee_acc_id = False
                self.show_native_accs2 = False
        else:
            self.rfc2 = False
            self.destiny_bank_id = False
            self.payee_acc_id = False
            self.show_native_accs2 = False
            
    """

    @api.onchange('destiny_account_id')
    def onchange_destiny_account_id(self):
        if self.destiny_account_id:
            partner_rfc = self.destiny_account_id.partner_id.vat
            self.destiny_bank_id = self.destiny_account_id.bank_id.id
            self.destiny_bank_key = self.destiny_account_id.bank_id.sat_bank_id.bic or False
            if partner_rfc:
                self.rfc2 = partner_rfc[2:] if len(partner_rfc) > 13 else partner_rfc
            if self._context.get('type_key', '') == 'transfer':
                self.payee_id = self.destiny_account_id.partner_id.id
                #self.payee_acc_id = self.destiny_account_id.bank_id.id                
                #self.show_native_accs2 = False
            else:
                self.payee_acc_id = False
                #self.show_native_accs2 = False
        else:
            self.rfc2 = False
            self.destiny_bank_id = False
            self.payee_acc_id = False
            self.destiny_bank_key = False
            #self.show_native_accs2 = False

    """
    @api.onchange('show_native_accs')
    def onchange_show_native_accs(self):
        if self.show_native_accs:
            self.onchange_origin_native_accid()
        else:
            self.onchange_origin_account_id()
            
            
    @api.onchange('show_native_accs1')
    def onchange_show_native_accs1(self):
        if self.show_native_accs1:
            self.onchange_destiny_native_accid()
        else:
            self.onchange_destiny_account_id()
            
    """
    
    
    @api.onchange('payee_id')
    def onchange_payee_id(self):
        if self._context.get('type_key', '') in ('payment', 'check'):
            if self.payee_id:
                payee_rfc = self.payee_id.vat
                if payee_rfc:
                    self.rfc2 = payee_rfc[2:] if len(payee_rfc) > 13 else payee_rfc
            else:
                self.rfc2 = False
        elif self._context.get('type_key', '') == 'foreign':
            self.rfc2 = False

    
    @api.onchange('payee_acc_id')
    def onchange_payee_acc_id(self):
        if self._context.get('type_key', '') in ('payment', 'check'):
            if self.payee_acc_id:
                payee_rfc = self.payee_acc_id.vat
                if payee_rfc:
                    self.rfc2 = payee_rfc[2:] if len(payee_rfc) > 13 else payee_rfc
            else:
                self.rfc2 = False
        elif self._context.get('type_key', '') == 'foreign':
            self.rfc2 = False
            
            
    @api.onchange('rfc')
    def onchange_rfc(self):
        if self.rfc and not _RFC_PATTERN.match(self.rfc):
            raise UserError(_('Verifique su información\n\nEl R.F.C. "%s" no se apega a los lineamientos del SAT.') % (self.rfc))

    @api.onchange('rfc2')
    def onchange_rfc2(self):
        if self.rfc2 and not _RFC_PATTERN.match(self.rfc2):
            raise UserError(_('Verifique su información\n\nEl R.F.C. "%s" no se apega a los lineamientos del SAT.') % (self.rfc2))


    @api.onchange('cbb_series')
    def onchange_cbb_series(self):
        if self.cbb_series and not _SERIES_PATTERN.match(self.cbb_series):
            raise UserError(_('Verifique su información\n\nLa serie del comprobante solo puede contener letras de la A a la Z, sin incluir la Ñ.'))
        


    @api.onchange('uuid')
    def onchange_uuid(self):
        if self.uuid and not _UUID_PATTERN.match(self.uuid):
            raise UserError(_('Verifique su información\n\nEl UUID ingresado no se apega a los lineamientos del SAT.'))

    
    """
    @api.onchange('show_native_accs2')
    def onchange_show_native_accs2(self):
        if self.show_native_accs2:
            return self.onchange_payee_acc_id()
        else:
            return self.onchange_payee_id()
    """

    @api.onchange('file_data')
    def onchange_file_data(self, currency_id=False):
        if self.file_data:
            #### Migración CFDI 4.0 ####
            xml_data = base64.b64decode(self.file_data)
            version_cfdi = ""
            arch_xml = parseString(xml_data)

            try:
                cfdi_comprobante_att = arch_xml.getElementsByTagName('cfdi:Comprobante')[0]                    
            except:
                raise UserError(_('Formato de archivo incorrecto!\n\nSe necesita cargar un archivo de extensión ".xml" (CFDI)'))

            version_cfdi = cfdi_comprobante_att.attributes['Version'].value
            _logger.info("\n########### version_cfdi : %s" % version_cfdi)
            ###########################
            is_xml_signed = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')
            if not is_xml_signed:
                raise UserError(_('El XML no esta timbrado.'))
            cfdi_timbre_fiscal_digital = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
            
            uuid = cfdi_timbre_fiscal_digital.attributes['UUID'].value
                
            try:               
                cfdi_emisor = arch_xml.getElementsByTagName('cfdi:Emisor')[0]
            except:
                raise UserError(_('Estructura CFDI inválida\n\nNo se encontró el nodo "cfdi:Emisor"'))

            rfc_emisor = cfdi_emisor.attributes['Rfc'].value
            rfc_emisor = rfc_emisor.replace('&','&amp;')
            rfc_emisor = rfc_emisor.replace('<','&lt;')
            rfc_emisor = rfc_emisor.replace('>','&gt;')

            try:
                cfdi_receptor = arch_xml.getElementsByTagName('cfdi:Receptor')[0]
            except:
                raise UserError(_('Estructura CFDI inválida\n\nNo se encontró el nodo "cfdi:Receptor"'))

            rfc_receptor = cfdi_receptor.attributes['Rfc'].value
            rfc_receptor = rfc_receptor.replace('&','&amp;')
            rfc_receptor = rfc_receptor.replace('<','&lt;')
            rfc_receptor = rfc_receptor.replace('>','&gt;')

            monto_total_cfdi = float(cfdi_comprobante_att.attributes['Total'].value)

            try:
                fecha_cfdi = cfdi_comprobante_att.attributes['Fecha'].value
            except:
                fecha_cfdi = ""

            try:
                folio_cfdi = cfdi_comprobante_att.attributes['Folio'].value
            except:
                folio_cfdi = ""

            try:
                serie_cfdi = cfdi_comprobante_att.attributes['Serie'].value
            except:
                serie_cfdi = ""

            tipo_cambio = 1.0
            try:
                tipo_cambio = cfdi_comprobante_att.attributes['TipoCambio'].value
            except:
                tipo_cambio = tipo_cambio

            if not rfc_emisor:
                raise UserError(_('Información faltante\n\nNo se encontró el RFC emisor.'))

            if not rfc_receptor:
                raise UserError(_('Información faltante\n\nNo se encontró el RFC receptor.'))

            if not uuid:
                raise UserError(_('Información faltante\n\nNo se encontró el Folio Fiscal (UUID)'))

            if len(uuid) != 36:
                raise UserError(_('Información incorrecta\n\nEl Folio Fiscal (UUID) %s es incorrecto: se esperaban 36 caracteres, se encontraron %s' % (uuid, len(stampNode.attrib['UUID']))))
            
            self.uuid = uuid.upper()
            
            self.compl_currency_id = currency_id and currency_id.id or self.env.user.company_id.currency_id
            
            self.exchange_rate = float(tipo_cambio)

            self.cbb_series = serie_cfdi
            try:
                self.cbb_number = int(folio_cfdi)
            except:
                _logger.info("\n#### No es un valor numerico ")

            self.rfc = rfc_emisor
            self.rfc2 = rfc_receptor
            self.compl_date = fecha_cfdi
            self.amount = monto_total_cfdi
            return


    def onchange_attached(self, attachment=False, currency_id=False):
        if attachment:
            xml_data = base64.b64decode(attachment)
            version_cfdi = ""
            arch_xml = parseString(xml_data)

            vals = {}

            try:
                cfdi_comprobante_att = arch_xml.getElementsByTagName('cfdi:Comprobante')[0]                    
            except:
                raise UserError(_('Formato de archivo incorrecto!\n\nSe necesita cargar un archivo de extensión ".xml" (CFDI)'))

            version_cfdi = cfdi_comprobante_att.attributes['Version'].value
            _logger.info("\n########### version_cfdi : %s" % version_cfdi)
            ###########################
            is_xml_signed = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')
            if not is_xml_signed:
                raise UserError(_('El XML no esta timbrado.'))
            cfdi_timbre_fiscal_digital = arch_xml.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
            
            uuid = cfdi_timbre_fiscal_digital.attributes['UUID'].value
                
            try:               
                cfdi_emisor = arch_xml.getElementsByTagName('cfdi:Emisor')[0]
            except:
                raise UserError(_('Estructura CFDI inválida\n\nNo se encontró el nodo "cfdi:Emisor"'))

            rfc_emisor = cfdi_emisor.attributes['Rfc'].value
            rfc_emisor = rfc_emisor.replace('&','&amp;')
            rfc_emisor = rfc_emisor.replace('<','&lt;')
            rfc_emisor = rfc_emisor.replace('>','&gt;')

            try:
                cfdi_receptor = arch_xml.getElementsByTagName('cfdi:Receptor')[0]
            except:
                raise UserError(_('Estructura CFDI inválida\n\nNo se encontró el nodo "cfdi:Receptor"'))

            rfc_receptor = cfdi_receptor.attributes['Rfc'].value
            rfc_receptor = rfc_receptor.replace('&','&amp;')
            rfc_receptor = rfc_receptor.replace('<','&lt;')
            rfc_receptor = rfc_receptor.replace('>','&gt;')

            monto_total_cfdi = float(cfdi_comprobante_att.attributes['Total'].value)

            try:
                fecha_cfdi = cfdi_comprobante_att.attributes['Fecha'].value
            except:
                fecha_cfdi = ""

            try:
                folio_cfdi = cfdi_comprobante_att.attributes['Folio'].value
            except:
                folio_cfdi = ""

            try:
                serie_cfdi = cfdi_comprobante_att.attributes['Serie'].value
            except:
                serie_cfdi = ""

            if not rfc_emisor:
                raise UserError(_('Información faltante\n\nNo se encontró el RFC emisor.'))

            if not rfc_receptor:
                raise UserError(_('Información faltante\n\nNo se encontró el RFC receptor.'))

            if not uuid:
                raise UserError(_('Información faltante\n\nNo se encontró el Folio Fiscal (UUID)'))

            if len(uuid) != 36:
                raise UserError(_('Información incorrecta\n\nEl Folio Fiscal (UUID) %s es incorrecto: se esperaban 36 caracteres, se encontraron %s' % (uuid, len(stampNode.attrib['UUID']))))
            
            tipo_cambio = 1.0
            try:
                tipo_cambio = cfdi_comprobante_att.attributes['TipoCambio'].value
            except:
                tipo_cambio = tipo_cambio

            vals['uuid'] = uuid.upper()

            vals['compl_currency_id'] = currency_id and currency_id.id or self.env.user.company_id.currency_id.id
            vals['exchange_rate'] = float(tipo_cambio)

            vals['cbb_series'] = serie_cfdi

            try:
                vals['cbb_number'] =  int(folio_cfdi)
            except:
                _logger.info("\n#### No es un valor numerico ")
            vals.update({
                'rfc': rfc_emisor,
                'rfc2': rfc_receptor,
                'compl_date' : fecha_cfdi,
                'amount' : monto_total_cfdi,
            })
            return {'value':vals}
        return {'value':False}

class account_moveline_fit(models.Model):
    _inherit = 'account.move.line'

    complement_line_ids =  fields.One2many('eaccount.complements', 'move_line_id', string='Complementos')

    def unlink(self):    
        for move_line in self:
            move_line.complement_line_ids.unlink()
        return super(account_moveline_fit, self).unlink()
    
    def edit_eaccount_info(self):
        self.ensure_one()
        ctx = self._context.copy()
        ctx['c_amount'] = self.credit or self.debit
        ctx['c_date'] = self.move_id.date
        new_wizard = self.env['moveline.info.manager'].create({'line_id': self.id})
        return {
             'name'     : _('Información para contabilidad electrónica'),
             'type'     : 'ir.actions.act_window',
             'res_model': 'moveline.info.manager',
             'res_id'   : new_wizard.id,
             'view_mode': 'form',
             'view_type': 'form',
             'target'   : 'new',
             'context'  : ctx
                }




