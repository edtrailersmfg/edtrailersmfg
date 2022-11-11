# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http , _
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleSnippets(WebsiteSale):

    @http.route('/get/product_all/',type='json',auth='public',website=True)
    def get_all_product(self):
        products_template = request.env['product.template'].sudo().search([('sale_ok', '=', True),('is_published','=',True)])
        list_products = [{'id':i.id,'text':i.name,'image_url':request.website.image_url(i, 'image_512')} for i in products_template]
        return list_products

    @http.route('/get/product_detail/',type="json",auth='public',website=True)
    def get_product_name(self,**kwargs):
        product_id = int(kwargs.get('id'))
        get_products = request.env['product.template'].sudo().search([('id','=',product_id)])
        if(kwargs.get('name_only') == True):
            return get_products.name
        elif(kwargs.get('popover') == True):
            product_result = request.env['ir.ui.view']._render_template(
                'website_ecommerce_snippets_blocks_ul_73lines.hotspot_img_tmplt',{'product':get_products,'cls':kwargs.get('popstyle')})
            return product_result
        return True