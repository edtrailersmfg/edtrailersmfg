# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.


from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteProductQuick(WebsiteSale):

    def get_attribute_value_ids(self, product):
        """ list of selectable attributes of a product

        :return: list of product variant description
           (variant id, [visible attribute ids], variant price,
           variant sale price)
        """
        # product attributes with at least two choices
        product = product.with_context(quantity=1)

        visible_attrs_ids = product.attribute_line_ids.filtered(
            lambda l: len(l.value_ids) > 1).mapped('attribute_id').ids
        to_currency = request.website.get_current_pricelist().currency_id
        attribute_value_ids = []
        for variant in product.product_variant_ids:
            a = variant.product_tmpl_id._get_combination_info(
                combination=False, product_id=variant.id, add_qty=1,
                pricelist=False,
                parent_combination=False, only_template=False)
            if to_currency != product.currency_id:
                price = variant.currency_id._convert(
                    a.get('list_price'), to_currency, request.env.user.company_id, datetime.today())
            else:
                price = a.get('list_price')
            visible_attribute_ids = [v.id for v in variant.product_template_attribute_value_ids
                                     if v.attribute_id.id in visible_attrs_ids]
            attribute_value_ids.append([variant.id, visible_attribute_ids,
                                        a.get('list_price'), price])
        return attribute_value_ids

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteProductQuick, self).shop(page=page,
                                                    category=category,
                                                    search=search, ppg=ppg,
                                                    **post)
        res.qcontext.update({
            'get_attribute_value_ids': self.get_attribute_value_ids,
        })
        return res

    @http.route('/shop/quick/view', type='json', auth='public', website=True)
    def get_shop_page_product_quick_view_content(self, options, **kwargs):
        product_id = options.get('productID')
        product = request.env['product.template'].search([('id', '=', product_id)], limit=1)
        if not product:
            return []
        return request.env["ir.ui.view"]._render_template(
            'website_product_quick_view_ul_73lines.ul_quick_view_popup_modal_shop',
            {'product': product, 'base_url': request.env.user.get_base_url()})

    @http.route('/shop/cart/view', type='json', auth='public', website=True)
    def get_shop_page_product_cart_content(self, options, **kwargs):
        product_id = options.get('productCartID')
        product = request.env['product.template'].search([('id', '=', product_id)], limit=1)
        if not product:
            return []
        return request.env["ir.ui.view"]._render_template(
            'website_product_quick_view_ul_73lines.ul_cart_popup_modal_shop',
            {'product': product, 'base_url': request.env.user.get_base_url()})