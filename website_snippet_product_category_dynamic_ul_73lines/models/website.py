from odoo import api, fields, models


class ProductDynamicCategory(models.Model):
    _inherit = ['product.public.category']
    _name = 'product.public.category'

    visible_in_snippet = fields.Boolean(string='Visible In Snippet ?',default=True)

