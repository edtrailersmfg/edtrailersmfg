# -*- encoding: utf-8 -*-
#

{
    "name"      : "Contra Recibos de Facturas (Clientes y Proveedores)",
    "version"   : "1.0",
    "author"    : "Argil Consulting",
    "website"   : "https://argil.mx",
    "description" : """
Contra Recibos de Facturas (Clientes y Proveedores)
===================================================

Este módulo agrega la funcionalidad de Control de Contra-recibos para
las Facturas (tanto de Clientes como de Proveedores), además se 
re-calculan las fechas de vencimiento según la fecha del Contra-Recibo.

También agrega una validación para que no permita pagar Facturas
(de proveedores solamente) si no tiene asociado un Contra-recibo.

    """,
    
    "category"  : "Accounting",
    "depends"   : [
                    "account", 
                    ],
    "demo": [],
    "test": [],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter.xml",
        "data/ir_sequence_view.xml",
        "views/account_invoice_counter_receipt_view.xml",
        "views/account_invoice_view.xml",
        "report/account_invioce_counter_receipt_report.xml"
    ],
    "installable": True,
    
}
