# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Miscellaneous Options',
    'summary': 'MISC Options like... Tags, Brands, View Limit, '
               'View Switcher, Price Filter',
    'description': 'MISC Options like... Tags, Brands, View Limit, '
                   'View Switcher, Price Filter',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
	    'data/brand_menu_data.xml',
        'data/ribbon_style_data.xml',

        # 'views/product_limit_data.xml',
        # 'views/assets.xml',
        'views/templates.xml',
        # 'views/product_limit_view.xml',
        'views/product_views.xml',
        'views/brand_list_template.xml',
        'views/res_config_settings.xml',
    ],
    'demo': [
    ],
    'images': [
        'static/description/website_product_misc_options_ul_73lines.png',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_product_misc_options_ul_73lines/static/src/scss/ion.rangeSlider.css',
            '/website_product_misc_options_ul_73lines/static/src/scss/ion.rangeSlider.skinNice.css',
            '/website_product_misc_options_ul_73lines/static/src/scss/products_view_switcher.scss',
            '/website_product_misc_options_ul_73lines/static/src/scss/products_view_limit.scss',
            '/website_product_misc_options_ul_73lines/static/src/scss/brand_page.scss',
            '/website_product_misc_options_ul_73lines/static/src/scss/shop_page.scss',
            '/website_product_misc_options_ul_73lines/static/src/scss/product_cart_checkout.scss',
            '/website_product_misc_options_ul_73lines/static/src/js/ion.rangeSlider.js',
            '/website_product_misc_options_ul_73lines/static/src/js/products_view_limit.js',
            '/website_product_misc_options_ul_73lines/static/src/js/products_price_filter.js',
            '/website_product_misc_options_ul_73lines/static/src/js/products_tag_filter.js',
            '/website_product_misc_options_ul_73lines/static/src/js/filter_slidebar.js',
            '/website_product_misc_options_ul_73lines/static/src/js/cart_slidebar.js',
            '/website_product_misc_options_ul_73lines/static/src/js/cart_update.js',
            '/website_product_misc_options_ul_73lines/static/src/js/product_category.js',
            '/website_product_misc_options_ul_73lines/static/src/js/sticky_cart.js',

        ]
    },
    'installable': True,
    'price': 99,
    'license': 'OPL-1',
    'currency': 'EUR',
}
