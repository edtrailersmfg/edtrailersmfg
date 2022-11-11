from odoo.addons.website_carousel_base_ul_73lines.models.website_snippet_filter import OBJ_FIELD_MAP
from odoo import models, _

OBJ_FIELD_MAP['product.public.category'] = ['name', 'image_1920:image', 'id']


class Website(models.Model):
    _inherit = "website"

    def _bootstrap_snippet_filters(self):
        super(Website, self)._bootstrap_snippet_filters()
        ir_filter = self.env.ref('website_snippet_product_category_carousel_ul_73lines.dynamic_snippet_product_category_filter', raise_if_not_found=False)
        if ir_filter:
            self.env['website.snippet.filter'].create({
                'filter_id': ir_filter.id,
                'field_names': 'name,image_1920:image',
                'limit': 16,
                'name': _('Category'),
                'website_id': self.id,
            })