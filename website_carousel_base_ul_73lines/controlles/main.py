from odoo import http, fields
from odoo.http import request
from odoo.osv import expression
from odoo.tools import escape_psql
from lxml import etree
import json


class CustomSnippetsBlogs(http.Controller):

    @http.route('/website/custom/snippet/products', type='json', auth='public', website=True)
    def get_custom_dynamic_filter_products(self, filter_id, template_key, limit=None, search_domain=None):
        dynamic_filter = request.env['website.snippet.filter'].sudo().search(
            [('id', '=', filter_id)] + request.website.website_domain()
        )
        return dynamic_filter and dynamic_filter.product_render(template_key, limit, search_domain) or ''

    @http.route('/website/custom/snippet/filter_templates', type='json', auth='public',
                website=True)
    def get_custom_dynamic_snippet_templates(self, filter_name=False):
        domain = [['key', 'ilike', '.dynamic_filter_template_custom'], ['type', '=', 'qweb']]
        if filter_name:
            domain.append(['key', 'ilike', escape_psql('_%s_' % filter_name)])
        templates = request.env['ir.ui.view'].sudo().search_read(domain, ['key', 'name',
                                                                          'arch_db'])

        for t in templates:
            children = etree.fromstring(t.pop('arch_db')).getchildren()
            attribs = children and children[0].attrib or {}
            t['numOfEl'] = attribs.get('data-number-of-elements')
            t['numOfElSm'] = attribs.get('data-number-of-elements-sm')
            t['numOfElFetch'] = attribs.get('data-number-of-elements-fetch')
        return templates
