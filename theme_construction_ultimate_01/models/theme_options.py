# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import models

class ThemeConstructionUltimate01_Ultimate(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_construction_ultimate_01_post_copy(self, mod):
        self.disable_view('website.template_header_default')
        self.enable_view('website_customize_theme_business_ul_73lines.template_navbar_1')
        self.enable_view('theme_construction_ultimate_01.construction_theme_footer')
        self.enable_view('website_business_snippet_blocks_core_ul_73lines.copyright_2')
        self.enable_view('website.header_language_selector')
        self.enable_view('website.header_language_selector_no_text')
        self.enable_view('website.option_footer_scrolltop')
        self.enable_view('website.template_footer_slideout')