from odoo import http
from odoo.http import request


class WebsiteSale(http.Controller):

    @http.route('/shop/onchange/variant', type='json', auth='public')
    def shop_page_on_change_variant(self, product_id, **post):
        vals = request.env['product.template.attribute.value'].sudo().search([
            # ('ptav_active', '=', False),
            ('product_tmpl_id', '=', int(product_id)),
            ('attribute_id', '=', int(post.get('attribute_id'))),
            ('product_attribute_value_id', '=', int(post.get('product_attribute_value_id')))], limit=1)
        product_product = request.env['product.product'].sudo().search([
            ('product_template_variant_value_ids', 'in', vals.ids),
            ('product_tmpl_id', '=', int(product_id)),
        ], limit=1)
        href = '/web/image/product.product/%s/image_256' % product_product.id
        return href
