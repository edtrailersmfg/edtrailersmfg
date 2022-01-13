# -*- encoding: utf-8 -*-
#
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import base64
import logging
_logger = logging.getLogger(__name__)

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
    
    partner_parent_id = fields.Many2one('res.partner', related='partner_id.parent_id', string='Parent Partner')
    cmpl_type       = fields.Selection([('check', 'Cheque'), 
                                        ('transfer', 'Transferencia'), 
                                        ('payment', 'Otro método de pago')], 
                                       string='Tipo de complemento', 
                                       help='Indique el tipo de complemento a usar para este pago.')
    other_payment   = fields.Many2one('eaccount.payment.methods', string='Método de Pago SAT')

    
    
    def _create_payment_vals_from_wizard(self):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        _logger.info("res: %s" % res)
        res.update({
            'cmpl_type' : self.cmpl_type,
            'other_payment' : self.other_payment.id,
        })        
        return res

    @api.onchange('cmpl_type')
    def _onchange_cmpl_type(self):
        if self.cmpl_type == 'check':
            self.pay_method_id = self.env['pay.method'].search([('code','=','02')], limit=1)
        elif self.cmpl_type == 'transfer':
            self.pay_method_id = self.env['pay.method'].search([('code','=','03')], limit=1)
            
    @api.onchange('other_payment')
    def _onchange_other_payment(self):
        rel = {'01' : '01',
               '02' : '02',
               '03' : '03',
               '04' : '04',
               '05' : '05',
               '06' : '06',
               '07' : False,
               '08' : '08',
               '09' : False,
               '10' : False,
               '11' : False,
               '12' : '12',
               '13' : '13',
               '14' : '14',
               '15' : '15',
               '16' : False,
               '17' : '17',
               '98' : '98',
               '99' : '99',
               '28' : '28',
               False: False,
              }
        self.pay_method_id = self.other_payment and rel[self.other_payment.code] and \
                             self.env['pay.method'].search([('code','=',rel[self.other_payment.code])], limit=1) or False

            

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    partner_parent_id = fields.Many2one('res.partner', related='partner_id.parent_id', string='Parent Partner')
    cmpl_type       = fields.Selection([('check', 'Cheque'), 
                                        ('transfer', 'Transferencia'), 
                                        ('payment', 'Otro método de pago')], 
                                       string='Tipo de complemento',
                                       help='Indique el tipo de complemento a usar para este pago.')
    other_payment   = fields.Many2one('eaccount.payment.methods', string='Método de Pago SAT', readonly=True, states={'draft': [('readonly', False)]})
    
    complements_contae = fields.Boolean('Complementos ContaE')

    @api.onchange('journal_id')
    def _onchange_journal_asti(self):
        # res = super(AccountPayment,self)._onchange_journal()
        if self.journal_id:
            self.cmpl_type = self.journal_id.cmpl_type or False
            self.other_payment = self.journal_id.other_payment or False
            # if self.journal_id.cmpl_type != 'check':
            #     self.check_number = False
        
    @api.onchange('cmpl_type')
    def _onchange_cmpl_type(self):
        pay_method_obj = self.env['pay.method']
        if self.cmpl_type == 'check':
            self.pay_method_id = pay_method_obj.search([('code','=','02')], limit=1)
        elif self.cmpl_type == 'transfer':
            self.pay_method_id = pay_method_obj.search([('code','=','03')], limit=1)
            
    @api.onchange('other_payment')
    def _onchange_other_payment(self):
        pay_method_obj = self.env['pay.method']
        rel = {'01' : '01',
               '02' : '02',
               '03' : '03',
               '04' : '04',
               '05' : '05',
               '06' : '06',
               '07' : False,
               '08' : '08',
               '09' : False,
               '10' : False,
               '11' : False,
               '12' : '12',
               '13' : '13',
               '14' : '14',
               '15' : '15',
               '16' : False,
               '17' : '17',
               '98' : '98',
               '99' : '99',
               '28' : '28',
               False: False,
              }
        self.pay_method_id = self.other_payment and rel[self.other_payment.code] and \
                             pay_method_obj.search([('code','=',rel[self.other_payment.code])], limit=1) or False

    
    def do_something_with_xml_attachment(self, attach):
        self.ensure_one()
        res = super(AccountPayment, self).do_something_with_xml_attachment(attach)        
        #attachment = attach
        line_id = [ ln.id for ln in self.move_id.line_ids if ln.account_id.internal_type == "liquidity" ]
        if len(line_id):            
            cmplObj = self.env['eaccount.complements']
            cmpl_vals = cmplObj.onchange_attached(attachment=attach.datas, currency_id=self.currency_id)['value']
            cmpl_vals['type_id'] = self.env['eaccount.complement.types'].search([('key', '=', 'cfdi')], limit=1).id
            cmpl_vals['type_key'] = 'cfdi'
            cmpl_vals['move_line_id'] = line_id[0]
            cmpl_vals['file_data'] = base64.decodebytes(attach.datas)
            cmplObj.create(cmpl_vals)            
        return res
    
    def get_cfdi(self):
        res = super(AccountPayment, self).get_cfdi()
        self.create_automatic_complements_eacounting()
        return res
    
    def action_post(self):
        move = super(AccountPayment, self).action_post()
        company = self.env.user.company_id
        if not company.auto_mode_enabled:
            return move
        # self.create_automatic_complements_eacounting()
        return move

    def create_automatic_complements_eacounting(self):
        company = self.env.user.company_id
        if not company.auto_mode_enabled:
            return True
        cmplObj = self.env['eaccount.complements']
        cmplTypeObj = self.env['eaccount.complement.types']
        _logger.info("\n\n* * * * * * * * * *\nSi entra")
        for payment in self:
            if not payment.cmpl_type:
                raise UserError("El Pago %s no cuenta con Tipo de Complemento. " % payment.name)
            if not payment.cfdi_folio_fiscal:
                raise UserError("El Pago %s aun no cuenta con Folio Fiscal UUID " % payment.name)
            _logger.info("OK 1")
            if payment.amount <= 0:
                raise UserError(_("No puede registrar un pago con monto cero, por favor revise y corrija..."))
            if not payment.cmpl_type: #  or payment.payment_type == 'transfer': Falta validar si se debe crear complemento o no
                continue
            _logger.info("OK 2")
            ## Obtenemos los valores base
            ## Inicio
            # Obtenemos la partida sobre la cual registrar el complemento
            line_id = [ ln for ln in payment.move_id.line_ids if ln.account_id.internal_type == 'liquidity' ]
            _logger.info("OK 3")
            if not line_id:
                _logger.warning("\n######## No se encontraron partidas de tipo liquidez, usaremos la cuenta Pendiente.")
                # raise ValidationError (_("Error!\nEste diario no deberia generar Complementos de Pago, debido a que no existe una cuenta de Tipo Liquidez."))
            line_id = [ ln for ln in payment.move_id.line_ids if ln.account_id.id == payment.outstanding_account_id.id ]
            _logger.info("OK 4")
            if not line_id:
                raise ValidationError (_("Error!\nEste diario no deberia generar Complementos de Pago, debido a que no existe una cuenta para generar la información de Contabilidad Electrónica."))
            if line_id[0].complement_line_ids:
                _logger.info("El Pago %s ya cuenta con Complementos de Contabilidad Electrónica. " % payment.name)
                return True

            cmpl_vals = {
                 'compl_currency_id': payment.currency_id.id,
                 'amount'           : payment.amount,
                 'compl_date'       : payment.date,
                 'type_id'          : cmplTypeObj.search([('key', '=', payment.cmpl_type)])[0].id,
                 'type_key'         : payment.cmpl_type
                }
            _logger.info("OK 5")
            curr_rate = payment.currency_id._convert(1.0, payment.company_id.currency_id, 
                                                     payment.company_id, payment.date)
            _logger.info("curr_rate %s " % curr_rate)
            cmpl_vals['exchange_rate'] = curr_rate
            if cmpl_vals['type_key'] == 'check':
                cmpl_vals['check_number'] = payment.check_number or payment.journal_id.check_next_number
            if cmpl_vals['type_key'] == 'payment':
                cmpl_vals['pay_method_id'] = payment.other_payment.id or payment.journal_id.other_payment.id
                
            cmpl_vals['move_line_id'] = line_id[0].id
            # Fin
            # Validaciones generales
            
            ## Cobros a Clientes y/o Devoluciones de Proveedores
            if payment.payment_type == 'inbound':
                _logger.info("**** inbound")
                # Datos Receptor
                cmpl_vals['rfc2'] = company.partner_id.vat
                if payment.journal_id.bank_account_id:
                    cmpl_vals['destiny_account_id'] = payment.journal_id.bank_account_id.id
                    destiny_bank = payment.journal_id.bank_id
                    cmpl_vals['destiny_bank_id'] = destiny_bank.id
                    cmpl_vals['destiny_bank_key'] = destiny_bank.sat_bank_id.bic
                    if destiny_bank.sat_bank_id.bic == '999':
                        cmpl_vals['destiny_frgn_bank'] = destiny_bank.name 
                if payment.cmpl_type in ('transfer','check'): # Se requieren TODOS los datos para el complemento
                    # Beneficiario
                    cmpl_vals['payee_id'] = company.partner_id.id 
                    # Datos Emisor
                    cmpl_vals['rfc'] = payment.partner_id.vat
                    #cmpl_vals['show_native_accs'] = True
                    if payment.cmpl_type == 'transfer' or (payment.cmpl_type == 'check' and payment.partner_bank_id):
                        cmpl_vals['origin_account_id'] = payment.partner_bank_id.id
                        origin_bank = payment.partner_bank_id and payment.partner_bank_id.bank_id or False
                        cmpl_vals['origin_bank_id'] = origin_bank and origin_bank.id or False
                        cmpl_vals['origin_bank_key'] = origin_bank and origin_bank.sat_bank_id and origin_bank.sat_bank_id.bic or False
                        if origin_bank and origin_bank.sat_bank_id and origin_bank.sat_bank_id.bic == '999':
                            cmpl_vals['origin_frgn_bank'] = origin_bank and origin_bank.name or origin_bank
                
                
                elif payment.cmpl_type == 'payment': # Otro metodo de pago (No es Trasnfer ni Cheque)
                    # Beneficiario
                    cmpl_vals['payee_id'] = company.partner_id.id 
                    # Datos Emisor
                    cmpl_vals['rfc'] = payment.partner_id.vat
                   
            
            ## Pagos a Proveedores y/o Devoluciones a Clientes
            elif payment.payment_type == 'outbound':
                _logger.info("**** outbound")
                _logger.info("Pagos a Proveedores y/o Devoluciones a Clientes")
                # Datos Emisor
                cmpl_vals['rfc'] = company.partner_id.vat
                if payment.journal_id.bank_account_id:
                    cmpl_vals['origin_account_id'] = payment.journal_id.bank_account_id.id
                    origin_bank = payment.journal_id.bank_id
                    cmpl_vals['origin_bank_id'] = origin_bank.id
                    cmpl_vals['origin_bank_key'] = origin_bank.sat_bank_id.bic
                    if origin_bank.sat_bank_id.bic == '999':
                        cmpl_vals['origin_frgn_bank'] = origin_bank.name
                if payment.cmpl_type in ('transfer','check'): # Se requieren TODOS los datos para el complemento
                    # Beneficiario
                    cmpl_vals['payee_id'] = payment.partner_id.id
                    # Datos Receptor
                    cmpl_vals['rfc2'] = payment.partner_id.vat
                    cmpl_vals['destiny_account_id'] = payment.partner_bank_id.id
                    #cmpl_vals['show_native_accs1'] = True
                    destiny_bank = payment.partner_bank_id.bank_id
                    cmpl_vals['destiny_bank_id'] = destiny_bank.id
                    cmpl_vals['destiny_bank_key'] = destiny_bank.sat_bank_id.bic
                    if destiny_bank.sat_bank_id.bic == '999':
                        cmpl_vals['destiny_frgn_bank'] = destiny_bank.name
            
                elif payment.cmpl_type == 'payment': 
                    # Beneficiario
                    cmpl_vals['payee_id'] = payment.partner_id.id 
                    
                    # Datos Receptor
                    cmpl_vals['rfc2'] = payment.partner_id.vat
                    if payment.partner_bank_id:
                        cmpl_vals['destiny_account_id'] = payment.partner_bank_id.id
                        #cmpl_vals['show_native_accs1'] = True
                        destiny_bank = payment.partner_bank_id.bank_id
                        cmpl_vals['destiny_bank_id'] = destiny_bank.id
                        cmpl_vals['destiny_bank_key'] = destiny_bank.sat_bank_id.bic
                        if destiny_bank.sat_bank_id.bic == '999':
                            cmpl_vals['destiny_frgn_bank'] = destiny_bank.name                
            
            ## Transferencias entre cuentas propias
            elif payment.payment_type == 'transfer':
                _logger.info("**** transfer")
                cmpl_vals['payee_id'] = company.partner_id.id
                cmpl_vals['rfc'] = company.partner_id.vat
                cmpl_vals['rfc2'] = company.partner_id.vat
                if payment.cmpl_type in ('transfer','check'):
                    # Datos Emisor
                    cmpl_vals['origin_account_id'] = payment.journal_id.bank_account_id.id
                    origin_bank = payment.journal_id.bank_id
                    cmpl_vals['origin_bank_id'] = origin_bank.id
                    cmpl_vals['origin_bank_key'] = origin_bank.sat_bank_id.bic
                    if origin_bank.sat_bank_id.bic == '999':
                        cmpl_vals['origin_frgn_bank'] = origin_bank.name
            
                if payment.destination_journal_id.cmpl_type in ('transfer','check'):
                    # Datos destino
                    cmpl_vals['destiny_bank_id'] = payment.destination_journal_id.bank_id.id
                    cmpl_vals['destiny_account_id'] = payment.destination_journal_id.bank_account_id.id
                    cmpl_vals['show_native_accs1'] = False                    
            _logger.info("**** OK 6")
            cmplObj.create(cmpl_vals)
            # item_concept = company._assembly_concept(payment.payment_type, voucher=payment)
            # _logger.info("**** item_concept: %s " % item_concept)
            # payment.move_id.item_concept = company._assembly_concept(payment.payment_type, voucher=payment)
            payment.complements_contae = True
            _logger.info("**** OK 7")
            #########
            xline_id = line_id[0].id
            if self._context.get('active_model') == 'account.move':
                for invoice in self.env['account.move'].browse(self._context.get('active_ids', [])).filtered(lambda w: w.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')):
                    for move_line in invoice.line_ids.filtered(lambda w: w.account_id.internal_type in ('receivable', 'payable')):
                        for complemento in move_line.complement_line_ids:
                            res = complemento.copy(default={'move_line_id': xline_id})
            

            #raise ValidationError("Pausa")
        return True


