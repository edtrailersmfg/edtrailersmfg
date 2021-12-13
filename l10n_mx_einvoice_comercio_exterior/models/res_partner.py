# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    cfdi_comercio_exterior_notas = fields.Text(string="Observaciones (Complemento Comercio Exterior)", copy=False)