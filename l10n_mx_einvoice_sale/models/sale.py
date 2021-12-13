# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'pay_method_id':self.partner_invoice_id.pay_method_id.id,
            #'acc_payment': self.partner_invoice_id.acc_payment and self.acc_payment.id or False,
            'uso_cfdi_id': self.partner_invoice_id.uso_cfdi_id.id,
            'metodo_pago_id' : self.payment_term_id and self.payment_term_id.metodo_pago_id and \
                                       self.payment_term_id.metodo_pago_id.id or False,
        })
        return invoice_vals
    
    