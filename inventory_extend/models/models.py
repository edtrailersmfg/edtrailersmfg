# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import datetime

class Product(models.Model):
    _inherit = "product.template"
    
    tipo_cambio = fields.Float(string="Tipo de Cambio", compute='_compute_tipo_cambio')
    costo_usd = fields.Float(string="Costo en USD", default=0)
    precio_usd = fields.Float(string="Precio de Venta USD", default=0)
    precio_mxn = fields.Float(string="Precio de Venta MXN", default=0)    


    def _compute_tipo_cambio(self):
        for product in self:
            ############
            # VAMOS A OBTENER EL TIPO DE CAMBIO
            ############
            tipo_de_cambio = 1.0
            reg_tc = self.env['res.currency.rate'].search([('id', '>', 0)], limit=1, order="id desc")
            if reg_tc:
                for record_tc in reg_tc:
                    tipo_de_cambio = record_tc.inverse_company_rate
            product['tipo_cambio'] = tipo_de_cambio
            product['costo_usd'] = product['standard_price'] / tipo_de_cambio
            precio_en_usd = 1.0
            precio_en_usd = ( (product['standard_price'] * 1.16) * 1.19 ) * 1.05
            product['precio_usd'] = precio_en_usd
            precio_en_mxn = precio_en_usd * tipo_de_cambio
            product['precio_mxn'] = precio_en_mxn
            product['list_price'] = precio_en_mxn

