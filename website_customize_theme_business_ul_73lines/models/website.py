# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WebsiteMenuRibbon(models.Model):
    _name = 'website.menu.ribbon.ultimate'
    _description = 'Website Menu Ribbon Ultimate'

    name = fields.Char(required=True, translate=True)
    menu_color_back = fields.Char(string='Background Color', required=True)
    menu_color_text = fields.Char(string='Font Color', required=True)

class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    menu_ribbon_id = fields.Many2one('website.menu.ribbon.ultimate', string='Ribbon Name')
    icon = fields.Char('Menu Icon')
    is_highlighted = fields.Boolean('Is Highlighted')
