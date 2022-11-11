# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import models

class ThemeLogisticsUltimate01_Ultimate(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_logistics_ultimate_01_post_copy(self, mod):
        self.disable_view('website.template_header_default')
        self.enable_view('website_customize_theme_business_ul_73lines.template_navbar_7')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_input_1')
        # self.enable_view('customize_theme_business.option_nav_transparent_font_default')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_nav_color_primary')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_mid_header_1')
        self.enable_view('theme_logistics_ultimate_01.logistics_theme_footer')
        self.enable_view('website_business_snippet_blocks_core_ul_73lines.copyright_1')
        self.enable_view('website.header_language_selector')
        # self.enable_view('website.header_language_selector_no_text')