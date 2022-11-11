# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import models

class ThemeBeautyEcommerceUltimate02_Ultimate(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_beauty_ecommerce_ultimate_02_post_copy(self, mod):
        self.disable_view('website.template_header_default')
        self.enable_view('website_customize_theme_business_ul_73lines.template_navbar_1')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_input_1')
        # self.enable_view('customize_theme_business.option_nav_transparent_font_default')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_nav_color_primary')
        # self.enable_view('customize_theme_business.option_mid_header_default')
        self.enable_view('theme_beauty_ecommerce_ultimate_02.beauty_two_ecommerce_theme_footer')
        self.enable_view('website_business_snippet_blocks_core_ul_73lines.copyright_5')
        # self.enable_view('website_customize_theme_business_ul_73lines.option_button_6')
        self.enable_view('website.header_language_selector')
        # self.enable_view('website.header_language_selector_no_text')
