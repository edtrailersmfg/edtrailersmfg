# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Page Layout',
    'summary': 'Product Page Layout',
    'description': 'Product Page Layout',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/product_attribute_view.xml',
    ],
    'images': [
        'static/description/website_product_page_layout_ul_73lines.png',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_product_page_layout_ul_73lines/static/src/scss/product_tab.scss',
            'website_product_page_layout_ul_73lines/static/src/js/main.js',
        ],
    },
    'installable': True,
    'price': 15,
    'license': 'OPL-1',
    'currency': 'EUR',
}
