# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ProductSizeChart(models.Model):
    _name = 'product.size.chart'
    _description = 'Product Size Chart'

    name = fields.Char(string='Name', required=True, translate=True)
    attribute_line = fields.One2many('product.size.attribute', 'chart_id')
    description = fields.Html("Description")

class ProductTemplate(models.Model):
    _inherit = "product.template"

    size_chart_ids = fields.Many2many('product.size.chart', string="Product's Size Chart")


class ProductSizeAttribute(models.Model):
    _name = "product.size.attribute"
    _description = "Product Size Attribute"

    name = fields.Char('Attribute', required=True, translate=True)
    chart_id = fields.Many2one('product.size.chart')
    sequence = fields.Integer(string='Sequence', help="Determine the display order", index=True)
    size_value_ids = fields.One2many('product.size.attribute.value', 'size_attribute_id', 'Values', copy=True)


class ProductSizeAttributeValue(models.Model):
    _name = "product.size.attribute.value"
    _order = 'sequence, id'
    _description = 'Attribute Size Value'

    name = fields.Char(string='Value', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', help="Determine the display order", index=True)
    size_attribute_id = fields.Many2one('product.size.attribute', string="Attribute", ondelete='cascade', required=True,
                                   index=True,
                                   help="The attribute cannot be changed once the value is used on at least one product.")
