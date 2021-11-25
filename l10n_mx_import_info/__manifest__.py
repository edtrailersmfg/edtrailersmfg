# -*- encoding: utf-8 -*-

{
    "name" : "Pedimentos Aduanales en CFDI",
    "version" : "1.0",
    "author" : "Argil Consulting",
    "category"  : "Localization",
    "website": "http://www.argil.mx",
    "description": """
Pedimentos Aduanales en CFDI
============================

Este módulo agrega el manejo de Pedimentos Aduanales en Facturación Electrónica


    """,
    "depends" : ["stock", "stock_account","account","sale_management", "purchase", "l10n_mx_einvoice"],
    "demo" : [],
    "data" : [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/import_info_view.xml',
        'views/stock_view.xml',
        'views/invoice_view.xml'
    ],

    "installable": True,
}
