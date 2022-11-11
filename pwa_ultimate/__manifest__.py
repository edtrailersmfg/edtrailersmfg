# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Ultimate PWA',
    'description': 'Ultimate Progressive Web App',
    'category': 'Corporate',
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    'depends': [
        'base_setup'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/web.xml',
        'views/pwa_config_view.xml',
        'views/res_config_settings.xml',
    ],
    'demo': [
        'demo/pwa_config_demo.xml',
    ],
    'assets': {
        'web.assets_common': [
            'pwa_ultimate/static/src/js/pwa.js',
        ],
    },
    'license': 'OPL-1',
    'currency': 'EUR',
    'live_test_url': 'https://www.73lines.com/r/vfd',
    'application': True,
}