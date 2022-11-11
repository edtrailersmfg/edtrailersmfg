# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Client Carousel Slider',
    'summary': 'Allows to drag & drop Client Carousel slider in website',
    'description': 'Allows to drag & drop Client Carousel slider in website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'depends': [
        'crm',
        'website_partner',
        'website_carousel_base_ul_73lines',
    ],
    'data': [
        'data/data.xml',
        'views/assets.xml',
        'views/snippets/snippets.xml',
        'views/snippets/s_clients.xml',
        'views/partner_view.xml',
    ],
    'images': [
        'static/description/website_client_carousel_slider_73lines.png',
    ],
    
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_client_carousel_ul_73lines/static/src/snippets/s_clients/000.js',
        ],
        'website.assets_wysiwyg': [
            '/website_snippet_client_carousel_ul_73lines/static/src/snippets/s_clients/options.js'
        ],
    },
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}


