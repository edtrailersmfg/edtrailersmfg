# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'

    carousel_ribbon_style = fields.Selection([
        ('ribbon_style_1', 'Ribbon Style 1'),
        ('ribbon_style_2', 'Ribbon Style 2'),
        ('ribbon_style_3', 'Ribbon Style 3'),
        ('ribbon_style_4', 'Ribbon Style 4'),
        ('ribbon_style_5', 'Ribbon Style 5'),
        ('ribbon_style_6', 'Ribbon Style 6'),
        ('ribbon_style_7', 'Ribbon Style 7'),
        ('ribbon_style_8', 'Ribbon Style 8'),
        ('ribbon_style_9', 'Ribbon Style 9'),
        ('ribbon_style_10', 'Ribbon Style 10')
    ], string='Carousel Ribbon Style', required=True)
