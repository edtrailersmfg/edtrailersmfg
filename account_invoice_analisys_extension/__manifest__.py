# -*- encoding: utf-8 -*-
###########################################################################
#
#    Copyright (c) 2015 Argil Consulting - http://www.argil.mx
#    All Rights Reserved.
############################################################################
#    Coded by: Israel CA (israel.cruz@argil.mx)

{
    "name": "Extensión - Análisis de Facturas", 
    "version": "1.0", 
    "author": "Argil Consulting", 
    "category": "Accounting", 
    "description": """

Extensión - Análisis de Facturas
==================================

Este módulo extiende el Análisis de Facturas

Se agregan las siguiente columnas:
    - 1/T.C. => 1.0 (Moneda base) / Tipo de Cambio (Moneda extranjera)
    - Saldo en Moneda de Factura
    - Referencia factura de Proveedor y/o Número de Factura de Cliente

    """, 
    "website": "http://www.argil.mx/", 
    #'license' : 'OEEL-1',
    "depends": ["account", "account_invoice_currency",
    ], 
    "data": [
        "account_invoice_report_view.xml"
    ], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}