# -*- coding: utf-8 -*-
{
    'name': "Control",

    'summary': """
            Modulo de Control de la Produccion
        """,

    'description': """
            Modulo de Control de la Produccion

            Capturamos informacion de los modulos de Ventas y Produccion para informar internamente la produccion
            y colocar informacion en el tablero web.

            Se genera un nuevo modelo production_data para registro de la producción en el piso de producción,
            esto permitirá actualizar el tablero de producción diaria.

    """,

    'author': "Enrique Jaquez",
    'website': "https://www.sursom.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '15.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'contacts', 'stock', 'product', 'mrp', 'logistics'],

    # always loaded
    'data': [
#        'security/ir.model.access.csv',
        'views/views.xml',
        'views/production_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
