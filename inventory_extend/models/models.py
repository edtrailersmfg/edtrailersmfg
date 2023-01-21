# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from datetime import datetime

class Product(models.Model):
    _inherit = "product.template"
    
    tipo_cambio = fields.Float(string="Tipo de Cambio", compute='_compute_tipo_cambio')
    fecha_actual = fields.Date(string="Fecha para TC", default=datetime.today())
    costo_usd = fields.Float(string="Costo USD", compute='_compute_costo_usd')
    utilidad_usd = fields.Float(string="Utilidad en USD", compute='_compute_utilidad_usd')
    utilidad = fields.Float(string="% de Utilidad", compute='_compute_utilidad')
    precio_usd = fields.Float(string="Precio de Venta USD", default=0)
    #precio_usd = fields.Float(string="Precio de Venta USD", compute='_compute_precio_usd')    

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    def _compute_tipo_cambio(self):
        for product in self:
            if product.tipo_cambio > 0:
                product['tipo_cambio'] = self.env['res.currency.rate'].search([ ('currency_id.name','=','USD'), ('name','=',self.fecha_actual) ]).inverse_company_rate

    def _compute_costo_usd(self):
        for product in self:
            if product.tipo_cambio > 0:
                product['costo_usd'] = self.standard_price / self.tipo_cambio

    def _compute_precio_usd(self):
        for product in self:
            product.precio_usd = 0
            if product.tipo_cambio > 0 & product.list_price > 0:
                product['precio_usd'] =  self.list_price / self.tipo_cambio
                
    def _compute_utilidad_usd(self):        
        for product in self:
            product['utilidad_usd'] = self.precio_usd - self.costo_usd

    def _compute_utilidad(self):        
        for product in self:
            product.utilidad = 0
            if product.costo_usd > 0:
                product['utilidad'] = ( self.utilidad_usd / self.costo_usd ) * 100


    @api.onchange('list_price')
    def _onchange_list_price(self):
        for product in self:
            if product.tipo_cambio > 0:
                product['precio_usd'] = self.list_price / self.tipo_cambio
                product['utilidad_usd'] = self.precio_usd - self.costo_usd
                if product.costo_usd > 0:
                    product['utilidad'] = ( self.utilidad_usd / self.costo_usd ) * 100


    @api.onchange('precio_usd')
    def _onchange_precio_usd(self):
        for product in self:
            product['list_price'] = self.precio_usd * self.tipo_cambio
            product['utilidad_usd'] = self.precio_usd - self.costo_usd
            if product.costo_usd > 0:
                product['utilidad'] = ( self.utilidad_usd / self.costo_usd ) * 100
            
