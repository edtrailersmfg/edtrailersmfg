# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wishlist_layout = fields.Selection([
        ('default', 'Default Wishlist'),
        ('ul_wishlist', 'Ultimate Wishlist'),
    ], string='Wishlist Page Layout',
        config_parameter='website_customize_theme_ecommerce_ul_73lines.wishlist_layout',
        default='default')
