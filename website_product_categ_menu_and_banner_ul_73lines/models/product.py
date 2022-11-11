# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.http import request


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    cover_banner = fields.Binary(string='Cover Banner')
    categ_title_background = fields.Char(string='Category Background Color')
    categ_title_color = fields.Char(string='Category Font Color')
    categ_icon = fields.Char('Category Icon')
    visible_in_menu = fields.Boolean(string='Visible In Menu ?', default=True)


class Website(models.Model):
    _inherit = 'website'

    def get_categories(self, search=''):
        category_counts = {}
        category_ids = self.env['product.public.category'].search(
            [('parent_id', '=', False)])
        product_category = self.env['product.public.category'].search([])
        for rec in product_category:
            categ = self.env['product.public.category'].search(
                [('parent_id', '=', rec.id)])
            print("--CATEGEEE", categ)
            count = self.env['product.template'].search_count([('public_categ_ids', 'in',
                                                               categ.ids + rec.ids)])
            category_counts[rec.id] = count
        res = {
            'categories': category_ids,
            'category_counts': category_counts,
        }
        return res
