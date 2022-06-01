# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    cost_amount = fields.Float(string="Cost Amount", compute="_compute_profit_margin", store=False, digits=(16, 2))
    price = fields.Float(string="Price", compute="_compute_profit_margin", store=False, digits=(16, 2))
    discount = fields.Float(string="Discount", compute="_compute_profit_margin", store=False, digits=(16, 2))
    profit = fields.Float(string="Profit", compute="_compute_profit_margin", store=False, digits=(16, 2))
    margin = fields.Float(string="Margin", compute="_compute_profit_margin", store=False, digits=(16, 2))

    @api.depends('invoice_line_ids', 'invoice_line_ids.profit', 'invoice_line_ids.margin', 'profit', 'amount_untaxed')
    def _compute_profit_margin(self):
        for rec in self:
            rec.cost_amount = sum(rec.invoice_line_ids.mapped('cost_amount'))
            rec.price     = sum(rec.invoice_line_ids.mapped('price'))
            rec.discount  = sum(rec.invoice_line_ids.mapped('discount'))
            rec.profit    = sum(rec.invoice_line_ids.mapped('profit'))
            rec.margin    = (rec.profit / rec.amount_untaxed) * 100 if rec.amount_untaxed else 0


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cost_amount = fields.Float(string="Cost Amount", compute="_custom_compute_cost_amount", digits=(16, 2))
    price = fields.Float(string="Price", compute="_custom_compute_cost_amount", digits=(16, 2))
    discount = fields.Float(string="Discount", compute="_custom_compute_cost_amount", digits=(16, 2))
    profit = fields.Float(string="Profit", compute="_compute_profit_margin", store=False, digits=(16, 2))
    margin = fields.Float(string="Margin", compute="_compute_profit_margin", store=False, digits=(16, 2))

    @api.depends('product_id', 'product_id.standard_price')
    def _custom_compute_cost_amount(self):
        for rec in self:
            #tomamos el dolar a $20 fijo para efecto de calculo
            rec.cost_amount = ( rec.product_id.standard_price / 20 ) * rec.quantity
            rec.price       = rec.price_unit * rec.quantity
            rec.discount    = rec.discount * rec.price

    @api.depends('cost_amount', 'product_id', 'product_id.standard_price')
    def _compute_profit_margin(self):
        for line in self:
            line.profit = line.price_subtotal - line.cost_amount
            line.margin = (line.profit / line.price_subtotal) * 100 if line.price_subtotal else 0
