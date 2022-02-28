# -*- coding: utf-8 -*-

from odoo import models, fields, api

class custom_partner(models.Model):

    _inherit = 'res.partner'

    #x_tipo = fields.Selection([
    #    ('Persona', 'Persona'),
    #    ('Organismo', 'Organismo')]
    #    ,required=True, default='Persona', string='Tipo')

