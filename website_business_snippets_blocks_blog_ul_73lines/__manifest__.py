# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Business Snippets Blocks Blog',
    'description': 'Business Snippets Blocks Blog',
    'version': '14.0.1.0.1',
    'category': "Business",
    'author': "73Lines",
    'website': 'https://www.73lines.com/',
    'depends': [

        # Default Modules
        'website_blog',

        # 73lines Depend Modules
        'website_snippet_blog_carousel_ul_73lines',
        'website_business_snippet_blocks_core_ul_73lines',


    ],
    'data': [
        'views/assets.xml',
        'views/snippets/blocks_blog.xml',
    ],
    'images': [
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_business_snippets_blocks_blog_ul_73lines/static/src/scss/blog_carousel.scss',
        ],
    },
    'price': 150,
    'currency': 'EUR',
    'license': 'OPL-1',
    'application': True
}
