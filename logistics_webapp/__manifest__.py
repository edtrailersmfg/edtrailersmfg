# -*- coding: utf-8 -*-
{
    'name': "Logistics Web App",

    'summary': """
        Aplication for Logistics Web Information""",

    'description': """
        Aplication for Logistics Web Information
    """,

    'author': "Sursoom",
    'website': "http://sursoom.mx/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mrp',
    'version': '14.2',

    # any module necessary for this one to work correctly
    'depends': ['base','website','contacts','logistics'],

    # always loaded
    'data': [
        'views/delivery_orders.xml',
        'views/delivery_order_form_template.xml',
        'views/do_thanking_template.xml',
    ],
    'js': [
        'static/src/js/website.js'
    ],


}
