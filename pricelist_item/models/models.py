from odoo import fields, api, models

class Pricelist_Items(models.Model):

    _inherit='product.pricelist.item'

    sequence = fields.Integer(default=10, string="Secuencia")

