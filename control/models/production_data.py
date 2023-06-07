# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class Production_Data(models.Model):
    _name = 'control.production_data'
    _description = "Datos levantados de Producción"

    serie = fields.Many2one('stock.production.lot', string="Serie")
    producto = fields.Many2one(related='serie.product_id', string="Producto")
    centro_trabajo = fields.Selection([
                ('No Iniciado','No Iniciado'),
                ('Producción','Producción'),
                ('Pintura','Pintura'),
                ('Ensamble','Ensamble'),
                ('Terminado','Terminado'),
                ('Hold','Hold'),
            ], string='Centro de Trabajo', 
               default='No Iniciado'
        )
    terminado = fields.Boolean(string='Terminado')
    hold = fields.Boolean(string='Hold')

    @api.onchange('centro_trabajo')
    def on_change_centro_trabajo(self):
        for record in self:
            if record.centro_trabajo == 'Terminado':
                record.terminado = True
            elif record.centro_trabajo == 'Hold':
                record.terminado = False
                record.hold = True
            else:
                record.terminado = False
                record.hold = False


