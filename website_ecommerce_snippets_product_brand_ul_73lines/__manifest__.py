# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Ecommerce Snippets Product Brand',
    'description': 'Ecommerce Snippets Product Brand',
    'category': "Ecommerce",
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
        'depends': [

        # Default Modules
        'website_sale',
        # 73lines Depend Modules
        'website_snippet_product_brand_carousel_ul_73lines',
        'website_business_snippet_blocks_core_ul_73lines',



    ],
    'data': [
        'views/assets.xml',
        'views/snippets/brand_carousel.xml',
    ],
    'images': [
        # 'static/description/pamela-ecommerce-banner.png',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_ecommerce_snippets_product_brand_ul_73lines/static/src/scss/product_brand_carousel.scss',
            '/website_ecommerce_snippets_product_brand_ul_73lines/static/src/scss/brand_carousel_design.scss',
        ],
    },
    # 'price': 50,
    # 'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': '',
    'application': True
}
