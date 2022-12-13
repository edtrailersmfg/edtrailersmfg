# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from datetime import datetime

class Product(models.Model):
    _inherit = "product.template"
    
    tipo_cambio = fields.Float(string="Tipo de Cambio", compute='_compute_tipo_cambio')
    fecha_actual = fields.Date(string="Fecha para TC", default=datetime.today())
    costo_usd = fields.Float(string="Costo USD", compute='_compute_costo_usd')
    utilidad = fields.Float(string="% de Utilidad")
    utilidad_usd = fields.Float(string="Utilidad en USD")
    precio_usd = fields.Float(string="Precio de Venta USD", compute='_compute_precio_usd')    

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    def _compute_tipo_cambio(self):
        for product in self:
            product['tipo_cambio'] = self.env['res.currency.rate'].search([ ('currency_id.name','=','USD'), ('name','=',self.fecha_actual) ]).inverse_company_rate

    def _compute_costo_usd(self):
        for product in self:
            if product.tipo_cambio > 0:
                product['costo_usd'] = self.standard_price / self.tipo_cambio
                product['utilidad_usd'] = self.precio_usd - self.costo_usd

    def _compute_precio_usd(self):
        for product in self:
            product.list_price = 0
            product['list_price'] = self.standard_price + ( self.standard_price * ( self.utilidad / 100 ) )
            if product.tipo_cambio > 0:
                product['precio_usd'] =  self.list_price / self.tipo_cambio
                product['utilidad_usd'] = self.precio_usd - self.costo_usd
                
    @api.onchange('utilidad')
    def _onchange_utilidad(self):
        if self.utilidad > 0:
            for product in self:
                product.list_price = 0
                product['list_price'] = self.standard_price + ( self.standard_price * ( self.utilidad / 100 ) )
                if product.tipo_cambio > 0:
                    product['precio_usd'] = self.list_price / self.tipo_cambio
                    product['utilidad_usd'] = self.precio_usd - self.costo_usd            

    @api.onchange('list_price')
    def _onchange_list_price(self):
        for product in self:
            product['utilidad'] = ( ( self.list_price - self.standard_price ) / self.standard_price ) * 100
            if product.tipo_cambio > 0:
                product['precio_usd'] = self.list_price / self.tipo_cambio
                product['utilidad_usd'] = self.precio_usd - self.costo_usd

