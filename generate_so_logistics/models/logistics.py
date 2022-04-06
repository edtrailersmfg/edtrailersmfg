# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomLogistica(models.Model):
    _inherit = 'logistica.ordenes_venta_carga'

    active = fields.Boolean(
        string='Active',
        default=True
    )
    estado = fields.Selection(
        selection_add=[('cancel', 'Cancel')]
    )
