# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Category Menu & Banner',
    'summary': 'Allows to add product category menu in Main menu nav-bar, '
               'Also allows to add product category banner in website',
    'description': 'Allows to add product category menu in Main menu nav-bar, '
                   'Also allows to add product category banner in website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': ['website_sale'],
    'data': [
        # 'views/assets.xml',
        'views/category_banner_template.xml',
        'views/category_menu_template.xml',
        'views/product_category_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_product_categ_menu_and_banner_ul_73lines/static/src/scss/category_banner.scss',
            '/website_product_categ_menu_and_banner_ul_73lines/static/src/scss/category_menu.scss',
        ]
    },
    'images': [
        'static/description/website_category_banner.png',
    ],
    'installable': True,
    'price': 30,
    'license': 'OPL-1',
    'currency': 'EUR',
}
