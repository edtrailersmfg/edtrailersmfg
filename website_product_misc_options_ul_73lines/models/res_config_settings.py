# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sticky_product_cart = fields.Selection([
        ('none', 'None'),
        ('style_one', 'Style One'),
        ('style_two', 'Style Two'),
        ('style_three', 'Style Three'),
    ], string='Sticky Product Cart',
        config_parameter='website_product_misc_options_ul_73lines.module_sticky_product_cart',
        default='none')

    product_name_row_limit = fields.Selection([
        ('one_line', 'One Line'),
        ('two_line', 'Two Line'),
        ('three_line', 'Three Line'),
    ], string='Row Limit for Product Name in Shop Page',
        config_parameter='website_product_misc_options_ul_73lines.product_name_row_limit',
        default='one_line')

    shop_page_list_view_style = fields.Selection([
        ('list_view_style_one', 'List View Style One'),
        ('list_view_style_two', 'List View Style Two'),
    ], string='List View Style for Shop Page',
        config_parameter='website_product_misc_options_ul_73lines.shop_page_list_view_style',
        default='list_view_style_one')
