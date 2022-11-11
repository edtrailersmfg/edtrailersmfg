# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Quick View',
    'summary': 'Website Product Quick View',
    'description': 'Website Product Quick View',
    'category': 'Website',
    'version': '15.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': ['website_sale'],
    'data': [
        'views/templates.xml',
    ],
    'images': [
        'static/description/website_product_quick_view_ul_73lines.jpg',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_product_quick_view_ul_73lines/static/scss/quick_view.scss',
            '/website_product_quick_view_ul_73lines/static/scss/cart_popup.scss',
            '/website_product_quick_view_ul_73lines/static/src/js/quick_view.js',
            '/website_product_quick_view_ul_73lines/static/src/js/cart_popup_view.js',
        ],
    },
    'installable': True,
    'price': 25,
    'license': 'OPL-1',
    'currency': 'EUR',
}
