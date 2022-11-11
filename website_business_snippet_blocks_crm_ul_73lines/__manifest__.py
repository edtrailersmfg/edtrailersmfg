# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Business Snippet Blocks CRM',
    'description': 'Business Snippet Blocks CRM',
    'category': "Business",
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    'depends': [
        'website',
        'website_crm',
        'website_business_snippet_blocks_core_ul_73lines'
    ],
    'data': [
        'views/assets.xml',

        #ContactUs Snippets
        'views/snippets/contactus/contact_us_1.xml',
        'views/snippets/contactus/contact_us_2.xml',
        'views/snippets/contactus/contact_us_3.xml',
        'views/snippets/contactus/contact_us_4.xml',
        'views/snippets/contactus/contact_us_5.xml',
        'views/snippets/contactus/contact_us_6.xml',
        'views/snippets/contactus/contact_us_7.xml',
        'views/snippets/contactus/contact_us_8.xml',
        'views/snippets/contactus/contact_us_9.xml',
        'views/snippets/contactus/contact_us_10.xml',
        'views/snippets/contactus/contact_us_11.xml',
        'views/snippets/contactus/contact_us_12.xml',
        'views/snippets/contactus/contact_us_13.xml',
        'views/snippets/contactus/contact_us_14.xml',
        'views/snippets/contactus/contact_us_15.xml',

    ],
    'demo': [
    ],
    'images': [
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_business_snippet_blocks_crm_ul_73lines/static/src/scss/crm.scss',
            '/website_business_snippet_blocks_crm_ul_73lines/static/src/scss/contact_us_3.scss',
            '/website_business_snippet_blocks_crm_ul_73lines/static/src/scss/contact_us_4.scss',
            '/website_business_snippet_blocks_crm_ul_73lines/static/src/scss/contact_us_14.scss',

            '/website_business_snippet_blocks_crm_ul_73lines/static/src/js/crm.js',

        ],
    },
    'price': 150,
    'license': 'OPL-1',
    'currency': 'EUR',
    'application': True,
}
