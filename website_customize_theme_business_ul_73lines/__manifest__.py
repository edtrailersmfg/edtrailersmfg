# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Customize Theme Business',
    'category': "Business",
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    'depends': [

        # Default Modules
        'theme_default',
        # 'google_dynamic_font',


    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/customize_model.xml',
        'views/navbar_headers.xml',
        'views/s_custom_button.xml',
        'views/language_selector.xml',
        'views/website_menu_ribbon.xml',
        'views/website_menu.xml',
        'views/website_menu_ribbon_template.xml',
        'views/website_view.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            '/website_customize_theme_business_ul_73lines/static/src/scss/navbar.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/divider.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/website_menu_ribbon.scss',
            '/website_customize_theme_business_ul_73lines/static/src/js/theme_custom.js',
            '/website_customize_theme_business_ul_73lines/static/src/scss/input_style.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/mid_header.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/button_style.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_pills.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_pills_square.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_pills_round.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_color_primary.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_strips.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_hover_top_border.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_hover_bottom_border.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/layout_fluid.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/nav_transparent.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/navbar_style.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/layout_fluid.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style1.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style2.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style3.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style4.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style5.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style6.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style7.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style8.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style9.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style10.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style11.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/side_navbar/style12.scss',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style1.js',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style2.js',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style3.js',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style4.js',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style5.js',
            '/website_customize_theme_business_ul_73lines/static/src/js/side_navbar/style6.js',
        ],
        'web._assets_primary_variables': [
            '/website_customize_theme_business_ul_73lines/static/src/scss/all_btn_design.scss',
            '/website_customize_theme_business_ul_73lines/static/src/scss/primary_variables.scss',
        ]
    },
    'price': 150,
    'license': 'OPL-1',
    'currency': 'EUR',
    'live_test_url': 'https://www.73lines.com/r/vfd',
    'application': True,
}

