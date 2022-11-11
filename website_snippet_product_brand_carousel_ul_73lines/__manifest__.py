# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Brand Carousel Slider',
    'summary': 'Allows to drag & drop Brand Carousel slider in website',
    'description': 'Allows to drag & drop Brand Carousel slider in website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': [
        'crm',
        'website_product_misc_options_ul_73lines',
        'website_carousel_base_ul_73lines'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'data': [
        'data/data.xml',
        'views/assets.xml',
        'views/snippets/snippets.xml',
        'views/snippets/s_brands.xml',
    ],
    'images': [
        'static/description/snippet_brand_carousel.jpg',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_product_brand_carousel_ul_73lines/static/src/snippets/s_brands/000.js',
        ],
        'website.assets_wysiwyg': [
            '/website_snippet_product_brand_carousel_ul_73lines/static/src/snippets/s_brands/options.js'
        ],
    },
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}


