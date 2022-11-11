from odoo.addons.website_carousel_base_ul_73lines.models.website_snippet_filter import OBJ_FIELD_MAP
from odoo import models, _

OBJ_FIELD_MAP['product.template'] = ['display_name', 'description_sale', 'image_512', 'list_price']


class Website(models.Model):
    _inherit = "website"

    def _bootstrap_snippet_filters(self):
        super(Website, self)._bootstrap_snippet_filters()
        ir_filter = self.env.ref('website_snippet_product_carousel_ul_73lines.dynamic_snippet_products_filter', raise_if_not_found=False)
        if ir_filter:
            self.env['website.snippet.filter'].create({
                'filter_id': ir_filter.id,
                'field_names': 'display_name,description_sale',
                'limit': 16,
                'name': _('Products'),
                'website_id': self.id,
            })
