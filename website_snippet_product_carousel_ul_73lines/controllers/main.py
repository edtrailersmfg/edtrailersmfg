from odoo import http,fields
from odoo.http import request
from odoo.osv import expression
import json


class CustomSnippetsBlogs(http.Controller):

    def get_rating_stat(self, product, context=None):
        rating_product = product.rating_get_stats([])
        return rating_product

    @http.route('/get/product_quick_view', type='json', auth='public', website=True)
    def get_product_quick_view_content(self, options, **kwargs):
        product_id = options.get('productID')
        product = request.env['product.template'].search([('id', '=', product_id)], limit=1)
        if not product:
            return []
        return request.env["ir.ui.view"]._render_template(
            'website_snippet_product_carousel_ul_73lines.product_quick_view_popup', {'product': product, 'base_url': request.env.user.get_base_url()})

    @http.route(['/shop/cart/update_continue'], type='http', auth="public",
                methods=['POST'], website=True)
    def cart_update_continue(self, product_id, add_qty=1, set_qty=0, **kw):
        sale_order = request.website.sale_get_order(force_create=True)
        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
        )
        return request.redirect(request.httprequest.referrer)
