# -*- coding: utf-8 -*-

{
    "name" : "Tipo de Cambio Manual en Odoo",
    "version" : "1.5",
    "depends" : [   
                    'base',
                    'account',
                    'l10n_mx_einvoice',
                    'l10n_mx_einvoice_comercio_exterior', # Si no usa Comercio Exterior quitarla
                    ],
    "author": "German Ponce Dominguez",
    "summary": "",
    "description": """

    Tipo de Cambio Manual en Odoo 15 Integrado con la LdM
    """,
    "price": 15,    
    "currency": "EUR",
    'category': 'Accounting',
    "website" : "https://poncesoft.blogpost.com",
    "data" :[
             "views/customer_invoice.xml",
             # "views/account_payment_view.xml",
    ],
    'qweb':[
    ],
    "auto_install": False,
    "installable": True,
    "license": "OPL-1",
}