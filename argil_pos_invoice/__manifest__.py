# -*- encoding: utf-8 -*-


{
    "name": "POS - Factura Diaria", 
    "version": "1.1", 
    "author": "Argil Consulting", 
    "category": "POS", 
    "description": """
POS - Factura Diaria
====================

Este módulo aplica para México. Si se registra una venta a través de TPV (POS) sin cliente
en particular entonces se debe crear una factura (diaria, semanal, mensual, esto lo define
la empresa) a CLIENTE PUBLICO EN GENERAL, por lo que este módulo ayuda en este punto.

También, cuando se crean Factura del POS, las partidas contables de la venta generada se
eliminan para evitar duplicidad de información.

Este módulo agrega un check en la Vista de Formulario del Cliente para poder marcarlo como
"Cliente Público en General". Si el cliente es seleccionado al registrar un Ticket de Venta
del POS entonces se tomará para crear la Factura Global, aunque esto dependerá de un Wizard
el cual mostrará todos los tickets por Facturar, si el ticket no tiene cliente asignado y/o
el Cliente asignado es "Cliente Publico en General" entonces todos los tickets con estas
características se agregarán a una sola Factura; los demás tickets con otro cliente asignado
crearán su propia factura, no se agrupará por cliente.

Configuracion:
==============

Es importante tener definido un Producto en la Contabilidad --> Configuracion --> Factura Global, que cumpla con las condiciones necesarias, unidad de Medida (ACT) y codigo producto (01010101), si este producto no existe se creara aumaticamente


    """, 
    "website": "http://www.argil.mx", 

    "depends": [#"base_setup", 
                "product", 
                "sale",
		        "account",
                "point_of_sale",
                "l10n_mx_einvoice",
            ], 
    "data": [
        "view/pos_invoice_view.xml",
        "view/sale_invoice_view.xml",
        "view/account_view_10.xml",
        "view/pos_order_view_10.xml",
        "view/global_concepts.xml",
        "security/ir.model.access.csv",
    ], 
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: