# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _name = 'account.move'
    _inherit ='account.move'



    currency_rate           = fields.Float(string='1/T.C.', digits=(12,4), compute="_get_tc_invoice", store=True)
    currency_rate2          = fields.Float(string='T.C.', digits=(12,4), compute="_get_tc_invoice", store=True)

    @api.depends('currency_id','invoice_date')
    def _get_tc_invoice(self):
        for move in self:
            if move.currency_id and move.currency_id.id != move.company_id.currency_id.id:
                cr = self.env.cr
                invoice_date = move.invoice_date if move.invoice_date else fields.Date.context_today(self)
                cr.execute("""
                    SELECT r.rate2, r.rate FROM res_currency_rate as r
                              WHERE r.currency_id = %s AND r.name <= %s
                                AND (r.company_id IS NULL OR r.company_id = %s)
                           ORDER BY r.company_id, r.name DESC
                              LIMIT 1
                    """, (move.currency_id.id, invoice_date, move.company_id.id, ))
                cr_res = cr.fetchall()
                if cr_res and cr_res[0] and cr_res[0][0]:
                    move.currency_rate = cr_res[0][1]
                    move.currency_rate2 = cr_res[0][0]
            else:
                move.currency_rate = 1.0
                move.currency_rate2 = 1.0

class account_invoice_report(models.Model):
    _inherit = "account.invoice.report"
    
    
    currency_rate           = fields.Float(string='1/T.C.', readonly=True, group_operator = 'avg')
    currency_rate2          = fields.Float(string='T.C.', readonly=True, digits=(12,4), group_operator = 'avg')
    price_subtotal_inv_curr = fields.Float(string='Subtotal en Moneda de Factura', readonly=True)
    residual2               = fields.Float(string='Saldo en Moneda de Factura', readonly=True)
    currency_id             = fields.Many2one('res.currency', string='Moneda')

    _depends = {
        'res.currency.rate': ['rate2','currency_id', 'name'],        
    }

    @api.model
    def _select(self):
        return  super(account_invoice_report, self)._select() + ", move.currency_rate, move.currency_rate2, move.currency_id, move.amount_untaxed price_subtotal_inv_curr, move.amount_residual residual2"


    def _group_by(self):
        return super(account_invoice_report, self)._group_by() + ", move.currency_rate, move.currency_rate2, move.currency_id, price_subtotal_inv_curr, residual2"

