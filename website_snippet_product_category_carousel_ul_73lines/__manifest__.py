# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Products Category Carousel Slider',
     'summary': 'Allows to drag & drop product category carousel '
                'slider in website',
     'description': 'Allows to drag & drop product category carousel '
                    'slider in website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': [
        'crm',
        'website_sale',
        'website_carousel_base_ul_73lines'
    ],
    'data': [
        'data/data.xml',
        'views/assets.xml',
        'views/snippets/s_category.xml',
        'views/snippets/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_product_category_carousel_ul_73lines/static/src/snippets/s_category/000.js',
        ],
        'website.assets_wysiwyg': [
            '/website_snippet_product_category_carousel_ul_73lines/static/src/snippets/s_category/options.js'
        ],
    },
    'images': [
        'static/src/description/snippet_product_category_carousel.jpg',
    ],
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}


