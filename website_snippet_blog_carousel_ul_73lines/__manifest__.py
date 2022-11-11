# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Blog Carousel Slider',
    'summary': 'Allows to drag & drop blog carousel slider in website',
    'description': 'Allows to drag & drop blog carousel slider in website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com/',
    'data': [
        'data/data.xml',
        'views/assets.xml',
        'views/snippets/snippets.xml',
        'views/snippets/s_blogs.xml',
        'views/blog_post_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'depends': ['website_blog',
                'website_carousel_base_ul_73lines'],
    'images': [
        'static/description/snippet_blog_carousel_73lines.jpg'
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_snippet_blog_carousel_ul_73lines/static/src/snippets/s_blog/000.js',
        ],
        'website.assets_wysiwyg': [
            '/website_snippet_blog_carousel_ul_73lines/static/src/snippets/s_blog/options.js'
        ],
    },
    'installable': True,
    'price': 20,
    'license': 'OPL-1',
    'currency': 'EUR',
}


