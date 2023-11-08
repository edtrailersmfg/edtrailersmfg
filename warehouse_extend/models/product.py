# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    warehouse01_quantity = fields.Char(compute='_get_warehouse_quantity', string='ALMACEN DE MATERIALES')
    warehouse02_quantity = fields.Char(string='ALMACEN EN PROCESO')

    def _get_warehouse_quantity(self):
        for record in self:
            warehouse_quantity_text = ''
            product_id = self.env['product.product'].sudo().search([('product_tmpl_id', '=', record.id)])
            if product_id:
                quant_ids = self.env['stock.quant'].sudo().search([('product_id','=',product_id[0].id),('location_id.usage','=','internal')])
                t_warehouses = {}
                for quant in quant_ids:
                    if quant.location_id:
                        if quant.location_id not in t_warehouses:
                            t_warehouses.update({quant.location_id:0})
                        t_warehouses[quant.location_id] += quant.quantity

                tt_warehouses = {}
                for location in t_warehouses:
                    warehouse = False
                    location1 = location
                    while (not warehouse and location1):
                        warehouse_id = self.env['stock.warehouse'].sudo().search([('lot_stock_id','=',location1.id)])
                        if len(warehouse_id) > 0:
                            warehouse = True
                        else:
                            warehouse = False
                        location1 = location1.location_id
                    if warehouse_id:
                        if warehouse_id.name not in tt_warehouses:
                            tt_warehouses.update({warehouse_id.name:0})
                        tt_warehouses[warehouse_id.name] += t_warehouses[location]

                for item in tt_warehouses:
                    if tt_warehouses[item] != 0:
                        if (item == "ALMACEN DE MATERIALES"):
                            warehouse_quantity_text = str(tt_warehouses[item])
                            record.warehouse01_quantity = warehouse_quantity_text
                        if (item == "ALMACEN EN PROCESO"):
                            warehouse_quantity_text = str(tt_warehouses[item])
                            record.warehouse02_quantity = warehouse_quantity_text

