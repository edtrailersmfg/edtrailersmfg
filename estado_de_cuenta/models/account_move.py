# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    cost_amount = fields.Float(string="Cost Amount", compute="_compute_profit_margin", store=False, digits=(16, 2))
    price = fields.Float(string="Price", compute="_compute_profit_margin", store=False, digits=(16, 2))
    price_mx = fields.Float(string="Precio MX", digits=(16, 2))
    tc = fields.Float(string="TC", digits=(16, 2))
    #vamos a calcular el descuento
    discount_invoice = fields.Float(string="Discount Invoice", compute="_compute_profit_margin", store=False, digits=(16, 2))
    profit = fields.Float(string="Profit", compute="_compute_profit_margin", store=False, digits=(16, 2))
    margin = fields.Float(string="Margin", compute="_compute_profit_margin", store=False, digits=(16, 2))

    @api.depends('invoice_line_ids', 'invoice_line_ids.profit', 'invoice_line_ids.margin', 'profit', 'amount_untaxed')
    def _compute_profit_margin(self):
        for rec in self:
            rec.cost_amount = sum(rec.invoice_line_ids.mapped('cost_amount'))
            rec.price       = sum(rec.invoice_line_ids.mapped('price'))

            if rec.amount_untaxed != rec.amount_untaxed_signed:
                rec.tc = rec.amount_untaxed_signed / rec.amount_untaxed
            else:
                rec.tc = 1.0
            rec.price_mx = rec.tc * rec.amount_untaxed

            #sumamos los descuentos que tiene
            rec.discount_invoice  = sum(rec.invoice_line_ids.mapped('discount_ammount'))
            #rec.profit    = sum(rec.invoice_line_ids.mapped('profit'))
            
            rec.profit   = rec.amount_untaxed_signed - rec.cost_amount
            rec.margin   = (rec.profit / rec.amount_untaxed_signed) * 100 if rec.amount_untaxed_signed else 0

            #rec.margin   = (rec.profit / rec.amount_untaxed) * 100 if rec.amount_untaxed else 0


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cost_amount = fields.Float(string="Cost Amount", compute="_custom_compute_cost_amount", digits=(16, 2))
    price = fields.Float(string="Price", compute="_custom_compute_cost_amount", digits=(16, 2))
    
    discount_ammount = fields.Float(string="Discount Ammount", compute="_custom_compute_cost_amount", digits=(16, 2))
    profit = fields.Float(string="Profit", compute="_compute_profit_margin", store=False, digits=(16, 2))
    margin = fields.Float(string="Margin", compute="_compute_profit_margin", store=False, digits=(16, 2))

    @api.depends('product_id', 'product_id.standard_price')
    def _custom_compute_cost_amount(self):
        for rec in self:
            rec.cost_amount      = rec.product_id.standard_price * rec.quantity
            rec.price            = rec.price_unit * rec.quantity
            rec.discount_ammount = (rec.discount / 100) * rec.price

    @api.depends('cost_amount', 'product_id', 'product_id.standard_price')
    def _compute_profit_margin(self):
        for line in self:
            line.profit = line.price_subtotal - line.cost_amount
            line.margin = (line.profit / line.price_subtotal) * 100 if line.price_subtotal else 0
