# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

    
class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
    

    @api.model
    def default_get(self, fields):
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')
        # Check for selected invoices ids
        if not active_ids or active_model != 'account.move':
            return super(AccountPaymentRegister, self).default_get(fields)
        xparam = self.env['ir.config_parameter'].get_param('account_invoice_counter_receipt_mandatory_for_payment', default='0')[0]
        if xparam != '1': # No se restringe que la factura tenga Contra-Recibo / Carta de Cobro para poder pagarla
            return super(AccountPaymentRegister, self).default_get(fields)
        
        invoices = self.env['account.move'].browse(active_ids)
        if all((invoice.counter_receipt_id and invoice.counter_receipt_id.state == 'confirmed') or \
                invoice.skip_counter_receipt_validation for invoice in invoices):
            return super(AccountPaymentRegister, self).default_get(fields)
        else:
            raise UserError(_("Aviso !\n\nNo puede realizar pagos sobre facturas que no tengan Contra-Recibo / Carta de Cobro o que no estén marcadas como 'No validar recepción'"))


class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    
    
    @api.model
    def default_get(self, fields):
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')        
        # Check for selected invoices ids
        if not active_ids or active_model != 'account.move':
            return super(AccountPayment, self).default_get(fields)
        xparam = self.env['ir.config_parameter'].get_param('account_invoice_counter_receipt_mandatory_for_payment', default='0')[0]
        if xparam != '1': # No se restringe que la factura tenga Contra-Recibo / Carta de Cobro para poder pagarla
            return super(AccountPayment, self).default_get(fields)
        
        invoices = self.env['account.move'].browse(active_ids)
        if all((invoice.counter_receipt_id and invoice.counter_receipt_id.state == 'confirmed') or \
                invoice.skip_counter_receipt_validation for invoice in invoices):
            return super(AccountPayment, self).default_get(fields)
        else:
            raise UserError(_("Aviso !\n\nNo puede realizar pagos sobre facturas que no tengan Contra-Recibo / Carta de Cobro o que no estén marcadas como 'No validar recepción'"))

