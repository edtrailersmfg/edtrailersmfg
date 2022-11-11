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
    ],
    'data': [
        # 'views/assets.xml',
        'views/snippets.xml',
        'views/product_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_product_category_dynamic_ul_73lines/static/src/scss/category_menu.scss',
            '/website_snippet_product_category_dynamic_ul_73lines/static/src/js/template_option.js',
        ]
    },
    'images': [
        'static/src/description/snippet_product_category_carousel.jpg',
    ],
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}


