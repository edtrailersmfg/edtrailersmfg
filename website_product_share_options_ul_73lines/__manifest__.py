# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Share Options',
    'summary': 'Allows to share product info in different Social Networks '
               'OR by Mail',
    'description': 'Allows to share product info in different Social Networks '
                   'OR by Mail',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': ['website_sale'],
    'data': [
        # 'views/assets.xml',
        'views/templates.xml',
    ],
    'images': [
        'static/description/website_product_share_button.jpg',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_product_share_options_ul_73lines/static/src/scss/share_buttons.scss',
        ]
    },
    'installable': True,
    'price': 10,
    'license': 'OPL-1',
    'currency': 'EUR',
}
