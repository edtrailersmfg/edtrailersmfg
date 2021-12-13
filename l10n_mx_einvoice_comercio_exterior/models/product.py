# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _, tools, release


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sat_arancel_id = fields.Many2one('sat.arancel', string="Fracción Arancelaria")
    sat_marca       = fields.Char('Marca')
    sat_modelo      = fields.Char('Modelo')
    sat_submodelo   = fields.Char('SubModelo')
    sat_factor_conversion = fields.Float(
        string="Factor Conversión", default=1.0, digits=0,
        help="Factor de Conversión para la Unidad de Medida por defecto del producto")