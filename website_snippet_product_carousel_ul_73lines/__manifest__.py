# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Products Carousel Slider',
    'summary': 'Allows to drag & drop 2 types of product carousel '
               'sliders in website'
               '1.) Product Carousel Slider'
               '2.) Product Mini Carousel Slider',
    'description': 'Allows to drag & drop 2 types of product carousel '
                   'sliders in website'
                   '1.) Product Carousel Slider'
                   '2.) Product Mini Carousel Slider',
    'category': 'Website',
    'version': '13.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'qweb': ['static/src/xml/*.xml'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/assets.xml',
        'views/snippets/snippets.xml',
        'views/snippets/dynamic_products.xml',
        # 'views/product_quick_view.xml',
        'views/product_view.xml',
        'views/product_ribbon_view.xml',
        'views/banner_with_product_carousel.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_product_carousel_ul_73lines/static/src/snippets/s_cart_products/000.js',
            '/website_snippet_product_carousel_ul_73lines/static/src/scss/product_carousel.scss'
        ],
        'website.assets_wysiwyg': [
            '/website_snippet_product_carousel_ul_73lines/static/src/snippets/s_cart_products/options.js'
        ],
    },
    'depends': ['website_sale_wishlist',
                'website_sale_comparison',
                'website_carousel_base_ul_73lines'],
    'images': [
        'static/description/snippet_product_carousel.jpg',
    ],
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}
