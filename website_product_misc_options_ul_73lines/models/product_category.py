# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.http import request


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    visible_in_shop_page = fields.Boolean(string='Visible In Shop Page ?', default=True)


class ProductQuickFilter(models.Model):
    _inherit = 'product.attribute'

    quick_filter = fields.Boolean(string='Visible in Quick Filter ?')