# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import models

class ThemeAppUltimate01_Ultimate(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_app_ultimate_01_post_copy(self, mod):
        self.disable_view('website.template_header_default')
        self.enable_view('website_customize_theme_business_ul_73lines.template_navbar_1')
        self.enable_view('theme_app_ultimate_01.app_theme_footer')
        self.enable_view('website_business_snippet_blocks_core_ul_73lines.copyright_1')
        self.enable_view('website.header_language_selector')
        self.enable_view('website.header_language_selector_inline')
        self.enable_view('website.header_language_selector_flag')
        self.enable_view('website.header_language_selector_no_text')
