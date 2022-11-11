# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _name = 'product.template'

    is_new = fields.Boolean(string='Is New ?')
    is_best_seller = fields.Boolean(string='Is Best Seller ?')
    is_trending = fields.Boolean(string='Is Trending ?')
    is_on_sale = fields.Boolean(String='Is On Sale ?')

    def get_rating_stat(self, product, context=None):
        rating_product = product.rating_get_stats()
        return rating_product