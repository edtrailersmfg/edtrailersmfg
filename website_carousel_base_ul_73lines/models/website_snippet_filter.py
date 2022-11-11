from ast import literal_eval
from odoo import models, fields, api, _
from odoo.osv import expression
from lxml import etree as ET
from odoo.exceptions import ValidationError, MissingError
from lxml import etree, html
import logging

_logger = logging.getLogger(__name__)

OBJ_FIELD_MAP = {}


class Website(models.Model):
    _inherit = 'website'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Website, self).create(vals_list)
        res._bootstrap_snippet_filters()
        return res

    def _bootstrap_snippet_filters(self):
        pass


class WebsiteSnippetFilter(models.Model):
    _inherit = 'website.snippet.filter'

    def product_render(self, template_key, limit, search_domain=[], with_sample=False):
        self.ensure_one()
        assert '.dynamic_filter_template_' in template_key, _("You can only use template prefixed by dynamic_filter_template_ ")
        if search_domain is None:
            search_domain = []

        if self.website_id and self.env['website'].get_current_website() != self.website_id:
            return ''

        if self.model_name.replace('.', '_') not in template_key:
            return ''

        records = self._prepare_product_values(limit, search_domain)
        is_sample = with_sample and not records
        if is_sample:
            records = self._prepare_sample(limit)
        View = self.env['ir.ui.view'].sudo().with_context(inherit_branding=False)
        content = View._render_template(template_key, dict(
            records=records,
            is_sample=is_sample,
        ))
        return [etree.tostring(el, encoding='unicode') for el in html.fromstring('<root>%s</root>' % str(content)).getchildren()]

    def _prepare_product_values(self, limit=None, search_domain=[]):
        """Gets the data and returns it the right format for render."""
        self.ensure_one()

        limit = limit and min(limit, self.limit) or self.limit
        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()
            if 'website_id' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, self.env[
                    'website'].get_current_website().website_domain()])
            if 'is_published' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [('is_published', '=', True)]])
            if search_domain:
                domain = expression.AND([domain, search_domain])
            try:
                records = self.env[filter_sudo.model_id].search(
                    domain,
                    order=','.join(literal_eval(filter_sudo.sort)) or None,
                    limit=limit
                )
                return records
            except MissingError:
                _logger.warning(
                    "The provided domain %s in 'ir.filters' generated a MissingError in '%s'",
                    domain, self._name)
                return []
        elif self.action_server_id:
            try:
                return self.action_server_id.with_context(
                    dynamic_filter=self,
                    limit=limit,
                    search_domain=search_domain,
                ).sudo().run() or []
            except MissingError:
                _logger.warning(
                    "The provided domain %s in 'ir.actions.server' generated a MissingError in '%s'",
                    search_domain, self._name)
                return []

    # For Filter Fields Onchange
    @api.onchange('filter_id')
    def onchange_filter_id(self):
        if self.filter_id:
            if self.filter_id.model_id in OBJ_FIELD_MAP:
                self.field_names = ",".join(OBJ_FIELD_MAP[self.filter_id.model_id])
        return OBJ_FIELD_MAP
