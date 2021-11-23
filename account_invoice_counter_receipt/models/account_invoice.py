# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    original_date_due   = fields.Date(string='Vencimiento Original', readonly=True, tracking=True,
                                     default=lambda self: self.invoice_date_due)
    
    skip_counter_receipt_validation = fields.Boolean(string="Sin Contra-Recibo", readonly=True,
                                                     tracking=True,
                                                     help="Active si no quiere manejar Contra-Recibo para esta factura", 
                                                     states={'draft': [('readonly', False)], 'open': [('readonly', False)]})
    
    counter_receipt_id = fields.Many2one('account.invoice.counter.receipt', 
                                         string="Contra-Recibo", readonly=True, tracking=True)
    
    counter_receipt_date = fields.Date(string="Fecha Contra-Recibo", related="counter_receipt_id.date", store=True)
    
    counter_receipt_state = fields.Selection(string="Contra-Recibo (Estado)", related="counter_receipt_id.state")
    
    
    
    
    
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    original_date_maturity   = fields.Date(string='Vencimiento Original', readonly=True, 
                                           default=lambda self: self.date_maturity)
    
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
