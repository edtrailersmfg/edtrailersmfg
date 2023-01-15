# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.margin', 'amount_untaxed')
    def _compute_margin(self):
        if not all(self._ids):
            for order in self:
                order.margin = sum(order.order_line.mapped('margin'))
                mapped_purchase_cost_data = sum(
                    order.order_line.mapped('purchase_price')
                )
                order.margin_percent = mapped_purchase_cost_data and order.margin / mapped_purchase_cost_data
        else:
            self.env["sale.order.line"].flush(['margin'])
            # On batch records recomputation (e.g. at install), compute the margins
            # with a single read_group query for better performance.
            # This isn't done in an onchange environment because (part of) the data
            # may not be stored in database (new records or unsaved modifications).
            grouped_order_lines_data = self.env['sale.order.line'].read_group([
                ('order_id', 'in', self.ids),
            ], ['margin', 'order_id', 'purchase_price'], ['order_id'])
            mapped_margin_data = {m['order_id'][0]: m['margin'] for m in grouped_order_lines_data}
            mapped_purchase_cost_data = {
                m['order_id'][0]: m['purchase_price'] for m in grouped_order_lines_data
            }
            for order in self:
                order.margin = mapped_margin_data.get(order.id, 0.0)
                order.margin_percent = mapped_purchase_cost_data and order.margin / mapped_purchase_cost_data.get(order.id, 0.0)
