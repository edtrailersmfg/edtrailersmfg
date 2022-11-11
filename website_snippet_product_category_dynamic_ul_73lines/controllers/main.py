from odoo import http
from odoo.http import request


class WebsiteSnippetTemplate(http.Controller):

    @http.route(['/snippet/get_template_data'], type='json', auth='public', website=True)
    def render_latest_posts(self, template, object=None):
        data = request.env[object].search([])
        return request.website.viewref(template)._render({'data': data})