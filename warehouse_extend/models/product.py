# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    warehouse01_quantity = fields.Float(compute='_get_warehouse_quantity', string='ALMACEN DE MATERIALES')
    warehouse02_quantity = fields.Float(string='ALMACEN EN PROCESO')

    def _get_warehouse_quantity(self):
        for record in self:
            x_warehouse01_quantity = 0
            x_warehouse02_quantity = 0
            product_id = self.env['product.product'].sudo().search([('product_tmpl_id', '=', record.id)])
            if product_id:
                quant_ids = self.env['stock.quant'].sudo().search([('product_id','=',product_id[0].id),('location_id.usage','=','internal')])
                #t_warehouses = {}
                for quant in quant_ids:
                    if quant.location_id:
                        #raise UserError( quant.location_id.name )
                        if quant.location_id.name == "StockMP":
                            x_warehouse01_quantity = quant.quantity
                        if quant.location_id.name == "StockPRO":
                            x_warehouse02_quantity = quant.quantity
                record.warehouse01_quantity = x_warehouse01_quantity
                record.warehouse02_quantity = x_warehouse02_quantity


