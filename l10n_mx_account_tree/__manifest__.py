# -*- encoding: utf-8 -*-
#

{
    "name": "Estructura Jerárquica de cuentas",
    "version": "1.0",
    "depends": [
        'account', 'analytic'
    ],
    "author": "Argil Consulting",
    "description" : """
Estructura Jerárquica de cuentas
================================

Este módulo agrega algunos cambios para obtener un Catálogo de Cuentas Jerárquico
para el Plan Contable y Cuentas Analíticas

    """,
    "website": "http://argil.mx",
    "category": "Accounting",
    "demo": [],
    "test": [],
    "data": [
        'security/ir.model.access.csv',
        'views/account_view.xml',
        'views/analytic_view.xml',
    ],
    "installable": True,

}
