# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if res:
            self.env['logistica.ordenes_venta_carga'].create({'orden_venta': self.id,})
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if res:
            delivery = self.env['logistica.ordenes_venta_carga'].search([('orden_venta', '=', self.id)])
            if delivery:
                delivery.write({'estado': 'cancel'})
        return res
