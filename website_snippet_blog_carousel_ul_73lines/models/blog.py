# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

import json
from odoo import api, fields, models, _


class WebsiteCoverPropertiesMixinInherit(models.AbstractModel):
    _inherit = 'blog.post'

    background_url = fields.Text('Background Url', compute='_compute_background_url')

    @api.depends('cover_properties')
    def _compute_background_url(self):
        for rec in self:
            val = json.loads(rec.cover_properties)
            if val['background-image'] == 'none':
                rec.background_url = 'none'
            else:
                rec.background_url = val['background-image']
