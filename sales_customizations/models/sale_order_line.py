# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    total_cost = fields.Float(string='Total Cost')

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            line.purchase_price = line.product_id.costo_usd
            line.total_cost = line.purchase_price * line.product_uom_qty
            line.margin = line.price_subtotal - (
                    line.purchase_price * line.product_uom_qty
            )
            if line.purchase_price > 0:
                if line.product_uom_qty > 0:
                    line.margin_percent = line.purchase_price and line.margin / ( line.purchase_price * line.product_uom_qty )
                else:
                     line.margin_percent = 0               
            else:
                line.margin_percent = 0