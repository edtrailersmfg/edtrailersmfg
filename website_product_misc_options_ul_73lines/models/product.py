# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class ProductTemplateSale(models.Model):
    _inherit = 'product.template'

    image_hover = fields.Image("Image on Hover")

    def _get_product_categories_count(self, website_ids, product_ids=[]):
        query_string = ' '
        if product_ids:
            query_string = ' FILTER (WHERE product_template.id in %(product_ids)s ) '
        else:
            query_string = ' FILTER (WHERE product_template.active = true AND (product_template.website_id in %(website_ids)s OR product_template.website_id is NULL))'

        query = """
                SELECT
                    count(product_template.id) """ + query_string + """,
                    min(product_public_category.parent_path) as path,
                    min(product_public_category.parent_id) as parent_id,
                    product_public_category.id as product_public_category_id
                FROM product_public_category_product_template_rel
                    JOIN product_template ON product_template.id = product_public_category_product_template_rel.product_template_id
                    RIGHT JOIN product_public_category ON product_public_category.id = product_public_category_product_template_rel.product_public_category_id
                GROUP BY product_public_category.id;
            """

        self.env.cr.execute(query, {'website_ids': tuple(website_ids), 'product_ids': tuple(product_ids)})
        query_res = self.env.cr.dictfetchall()

        result_count = dict([(line.get('product_public_category_id'), 0) for line in query_res])

        for line in query_res:
            for line2 in query_res:
                if line.get('parent_id'):
                    path = '/%s/' % line.get('product_public_category_id')
                    if path in line2.get('path'):
                        result_count[line.get('product_public_category_id')] += line2.get('count')
                else:
                    path = '%s/' % line.get('product_public_category_id')
                    if line2.get('path').startswith(path):
                        result_count[line.get('product_public_category_id')] += line2.get('count')

        return result_count

    def _get_product_brand_count(self, website_ids=False, product_ids=[]):
        result = {}
        brands = self.env['product.brand'].search([])
        for brand in brands:
            domain = []
            if product_ids:
                domain += [('id', 'in', product_ids)]
            domain += [('brand_id', '=', brand.id), '|', ('website_id', 'in', website_ids), ('website_id', '=', False)]
            result[brand.id] = self.env['product.template'].search_count(domain)
        return result

    def _get_product_tag_count(self, website_ids=False, product_ids=[]):
        result = {}
        tags = self.env['product.tags'].search([])
        for tag in tags:
            domain = []
            if product_ids:
                domain += [('id', 'in', product_ids)]
            domain += [('tag_ids', '=', tag.id), '|', ('website_id', 'in', website_ids), ('website_id', '=', False)]
            result[tag.id] = self.env['product.template'].search_count(domain)
        return result

    def _get_product_attribute_count(self, website_ids=False, product_ids=[]):
        result = {}
        attributes = self.env['product.attribute.value'].search([])
        domain = []
        if product_ids:
            domain += [('id', 'in', product_ids)]
        for attribute in attributes:
            lines = self.env['product.template.attribute.line'].search([('value_ids', 'in',[attribute.id])])
            products = []
            for line in lines:
                if line.product_tmpl_id.id not in products:
                    products.append(line.product_tmpl_id.id)
            result[attribute.id] = len(products)
        return result

    extra_info = fields.Html(string='Extra Info')