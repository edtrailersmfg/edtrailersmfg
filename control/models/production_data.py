# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class Production_Data(models.Model):
    _name = 'control.production_data'
    _description = "Datos levantados de Producción"

    serie = fields.Many2one('control.control', string="Serie", stored=True)
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