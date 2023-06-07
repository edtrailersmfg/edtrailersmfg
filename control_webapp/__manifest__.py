# -*- coding: utf-8 -*-
{
    'name': "Control Web App",

    'summary': """
            Aplicación para capturar información de las series de los remolques mediante la Web
        """,

    'description': """
            Control Web App

            Aplicación para capturar información de las series de los remolques mediante la Web
            desde la página se captura la serie y se le indica la etapa de producción en la que se encuentra,
            si está terminado puede ser hold o puede ser terminado.
    """,

    'author': "Enrique Jaquez",
    'website': "https://www.sursom.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '15.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
#        'security/ir.model.access.csv',
        'views/views.xml',
    ], 
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
