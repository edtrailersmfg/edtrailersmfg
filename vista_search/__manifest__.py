# -*- coding: utf-8 -*-
{
    'name': "Vista Search",

    'summary': """
            Agregamos campos a las vistas Search para facilitar las búsquedas
        """,

    'description': """
            Agregamos campos a las vistas Search para facilitar las búsquedas
    """,

    'author': "Sursoom",
    'website': "http://www.sursom.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
