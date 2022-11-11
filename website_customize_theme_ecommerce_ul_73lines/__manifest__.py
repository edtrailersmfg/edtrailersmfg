# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Theme Customize Ecommerce',
    'description': 'Theme Customize Ecommerce',
    'category': "Ecommerce",
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    'depends': [

        # Dependency Modules
        'website_customize_theme_business_ul_73lines',
        'website_sale',
        'website_sale_wishlist',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assests.xml',
        'views/customize_model.xml',
        'views/navbar_headers.xml',
        'views/category_view_inherit.xml',
        'views/category_breadcrumbs.xml',
        'views/res_config_settings.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/common.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_page_common.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_2.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_3.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_4.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_5.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_10.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_11.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_12.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_13.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_14.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_15.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_16.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/mid_header_17.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_default.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_1.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_2.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_3.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_4.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_5.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/shop_style_6.scss',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/scss/navbar_ecommerce.scss',


            '/website_customize_theme_ecommerce_ul_73lines/static/src/js/wishlist.js',
            '/website_customize_theme_ecommerce_ul_73lines/static/src/js/website_sale.js',
        ]
    },
    'price': 150,
    'license': 'OPL-1',
    'currency': 'EUR',
    'application': True,
}

