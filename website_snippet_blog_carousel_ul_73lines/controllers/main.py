# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import http,fields
from odoo.http import request
from odoo.osv import expression
import json


class CustomSnippetsBlogs(http.Controller):

    @http.route(['/website_snippet_blog_carousel_ul_73lines/blog_content'], type='json', auth="public", website=True)
    def render_latest_posts(self, template, domain, limit=None, order='published_date desc'):
        dom = expression.AND([
            [('website_published', '=', True), ('post_date', '<=', fields.Datetime.now())],
            request.website.website_domain()
        ])
        if domain:
            dom = expression.AND([dom, domain])
        posts = request.env['blog.post'].search(dom, limit=limit, order=order)
        return request.website.viewref(template)._render({'posts': posts})

    @http.route('/website/custom/snippet/filters', type='json', auth='public', website=True)
    def get_custom_dynamic_filter(self, filter_id, template_key, limit=None, search_domain=None):
        dynamic_filter = request.env['website.snippet.filter'].sudo().search(
            [('filter_id', '=', filter_id)] + request.website.website_domain()
        )
        return dynamic_filter and dynamic_filter.render(template_key, limit, search_domain) or ''


    @http.route('/website/blog/snippet/filter_templates', type='json', auth='public', website=True)
    def get_dynamic_snippet_templates(self, filter_id=False):
        # todo: if filter_id.model -> filter template
        templates = request.env['ir.ui.view'].sudo().search_read(
            [['key', 'ilike', '.73_custom_blog_snippet'], ['type', '=', 'qweb']], ['key', 'name']
        )
        return templates
