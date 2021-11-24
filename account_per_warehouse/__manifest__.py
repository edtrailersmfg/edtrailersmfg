# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
{
    "name": "Cuenta Contable por Almacén / Ubicación (interna)", 
    "version": "1.1", 
    "author": "Argil Consulting", 
    "category": "Account", 
    "description": """
Cuenta Contable por Almacén / Ubicación (interna)
=================================================

Este módulo permite usar diferentes cuentas contables por Almacén / Ubicación (interna).

El comportamiento estándar de Odoo es crear Pólizas contables de Movimientos de Almacén
donde la Ubicación Origen no sea interna y la Ubicación Destino tampoco sea interna.
Además que la cuenta contable para Valorización de Inventario se toma de la configuración
de la Categoría de Producto (Cuenta de Valorización de Inventario) o en el Producto.

Este módulo permite mostrar el campo "Cuenta Contable Entrada/Salida" en las Ubicaciones
Internas para que al generar la póliza tome esta cuenta contable.
    """, 
    "website": "http://www.argil.mx", 
    "depends": ["stock_account", 
                'stock',
                'stock_landed_costs',
    ], 
    "demo": [], 
    "data": [
        "view/stock_location_view.xml"
    ], 
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 

}