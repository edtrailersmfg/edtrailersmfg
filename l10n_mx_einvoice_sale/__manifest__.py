# -*- encoding: utf-8 -*-

{
    "name" : "Integración de info de Facturación Electrónica con Ventas",
    "version" : "1.0",
    "author" : "Fixdoo",
    "category"  : "Localization",
    "website": "http://www.fixdoo.mx",
    "description": """
Integración de info de Facturación Electrónica con Ventas
=============================================================

Este módulo integra los Pedidos de Venta con la información necesaria para Facturación Electrónica


    """,
    "depends" : [
                 "sale",
                 "l10n_mx_einvoice",],
    "demo" : [],
    "data" : [
        #'views/sale_view.xml',
    ],

    "installable": True,
    'license': 'Other proprietary',
}
