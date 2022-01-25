# -*- coding: utf-8 -*-
# Coded by German Ponce Dominguez 
#     ▬▬▬▬▬.◙.▬▬▬▬▬  
#       ▂▄▄▓▄▄▂  
#    ◢◤█▀▀████▄▄▄▄▄▄ ◢◤  
#    █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬  
#    ◥ █████ ◤  
#     ══╩══╩═  
#       ╬═╬  
#       ╬═╬ Dream big and start with something small!!!  
#       ╬═╬  
#       ╬═╬ You can do it!  
#       ╬═╬   Let's go...
#    ☻/ ╬═╬   
#   /▌  ╬═╬   
#   / \
# Cherman Seingalt - german.ponce@outlook.com
{
    "name": "Reporte Electronico CFDI 3.3 Edtrailers",
    "version": "15.0.1.0.0",
    "category": "Report",
    "website": "http://fixdoo.mx",
    "author": "German Ponce Dominguez (Desarrollador)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "description": "Factura Electronica Edtrailers",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "account",
        "l10n_mx_einvoice",
        "l10n_mx_einvoice_comercio_exterior",
    ],
    "data": [
        'reports/report_invoice_mx.xml',
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
