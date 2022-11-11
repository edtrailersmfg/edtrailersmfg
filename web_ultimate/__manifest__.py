# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Ultimate Web Tools',
    'description': 'Ultimate Website Tools Business',
    'category': 'Corporate',
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    "category": "Hidden",
    'depends': ['website'],
    'data': [
        # 'views/assets.xml',
    ],
    'assets': {
            'web.assets_backend': [
                '/web_ultimate/static/src/scss/web_changes.scss',
                ],
    },
    'installable': True,
    'auto_install': True,
}
