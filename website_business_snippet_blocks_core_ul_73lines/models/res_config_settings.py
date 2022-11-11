# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_pwa_ultimate = fields.Boolean(string='Enable PWA')


class UltimateTheme(models.AbstractModel):
    _inherit = 'theme.utils'
    _description = 'Theme Utils'
    _auto = False


    @api.model
    def _reset_default_config(self):
        self._header_templates.extend([
            'website.template_header_hamburger',
            'website.template_header_vertical',
            'website.template_header_sidebar',
            'website.template_header_slogan',
            'website.template_header_contact',
            'website.template_header_boxed',
            'website.template_header_centered_logo',
            'website.template_header_image',
            'website.template_header_hamburger_full',
            'website.template_header_magazine',
            'website_customize_theme_business_ul_73lines.template_navbar_1',
            'website_customize_theme_business_ul_73lines.template_navbar_2',
            'website_customize_theme_business_ul_73lines.template_navbar_3',
            'website_customize_theme_business_ul_73lines.template_navbar_4',
            'website_customize_theme_business_ul_73lines.template_navbar_5',
            'website_customize_theme_business_ul_73lines.template_navbar_6',
            'website_customize_theme_business_ul_73lines.template_navbar_7',
            'website_customize_theme_business_ul_73lines.template_navbar_8',
            'website_customize_theme_business_ul_73lines.template_navbar_9',
            'website_customize_theme_business_ul_73lines.template_navbar_10',
            'website_customize_theme_business_ul_73lines.template_navbar_13',
            'website_customize_theme_business_ul_73lines.template_navbar_14',
            'website_customize_theme_business_ul_73lines.template_navbar_17',
            'website_customize_theme_business_ul_73lines.template_navbar_18',
            'website_customize_theme_business_ul_73lines.template_navbar_19',
            'website_customize_theme_business_ul_73lines.template_navbar_20',
            'website_customize_theme_business_ul_73lines.template_navbar_21',
            'website_customize_theme_business_ul_73lines.template_navbar_22',
            'website_customize_theme_business_ul_73lines.template_navbar_23',
            'website_customize_theme_business_ul_73lines.template_navbar_24',
            'website_customize_theme_business_ul_73lines.template_navbar_25',
            'website_customize_theme_business_ul_73lines.template_navbar_26',
            'website_customize_theme_business_ul_73lines.template_navbar_27',
            'website_customize_theme_business_ul_73lines.template_navbar_28',
            # Default one, keep it last
            'website.template_header_default',
        ])
        self._footer_templates.extend([
            'website.template_footer_descriptive',
            'website.template_footer_centered',
            'website.template_footer_links',
            'website.template_footer_minimalist',
            'website.template_footer_contact',
            'website.template_footer_call_to_action',
            'website.template_footer_headline',
            'website_business_snippet_blocks_core_ul_73lines.footer_1',
            'website_business_snippet_blocks_core_ul_73lines.footer_2',
            'website_business_snippet_blocks_core_ul_73lines.footer_3',
            'website_business_snippet_blocks_core_ul_73lines.footer_4',
            'website_business_snippet_blocks_core_ul_73lines.footer_5',
            'website_business_snippet_blocks_core_ul_73lines.footer_6',
            'website_business_snippet_blocks_core_ul_73lines.footer_7',
            'website_business_snippet_blocks_core_ul_73lines.footer_8',
            'website_business_snippet_blocks_core_ul_73lines.footer_9',
            'website_business_snippet_blocks_core_ul_73lines.footer_10',
            'website_business_snippet_blocks_core_ul_73lines.footer_11',
            'website_business_snippet_blocks_core_ul_73lines.footer_12',
            'website_business_snippet_blocks_core_ul_73lines.footer_13',
            'website_business_snippet_blocks_core_ul_73lines.footer_14',
            'website_business_snippet_blocks_core_ul_73lines.footer_15',
            'website_business_snippet_blocks_core_ul_73lines.footer_16',
            'website_business_snippet_blocks_core_ul_73lines.footer_17',
            'website_business_snippet_blocks_core_ul_73lines.footer_18',
            'website_business_snippet_blocks_core_ul_73lines.footer_19',
            'website_business_snippet_blocks_core_ul_73lines.footer_20',
            # Default one, keep it last
            'website.footer_custom',
        ])
        super(UltimateTheme, self)._reset_default_config()
