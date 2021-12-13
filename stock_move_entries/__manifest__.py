# -*- encoding: utf-8 -*-

##############################################################################
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
{
    "name": "Información Contable en Movimientos de Inventario", 
    "version": "1.1", 
    "author": "Argil Consulting", 
    "category": "Account", 
    "description": """
Información Contable en Movimientos de Inventario
=================================================

Este módulo crea la relación entre el objeto stock.move y account.move (pólizas creadas por movimientos de inventario)

Además agrega las siguientes funcionalidades:
    - Vista de Lista de Stock Quants => Suma de la Valorización de Inventario
    - Vista de Lista de Stock Moves  => Agrega dos campos: 
            * [Precio Unitario] => Que ya existe en el modelo stock.move
            * [Monto Movimiento] => Calcula [Precio Unitario] * [Cant. Producto] * Sign (Entradas es 1, Salidas -1)
        También agrega la Suma del Monto Movimiento
    
    """, 
    "website": "http://www.argil.mx", 
    "depends": [
        "stock_account",
    ], 
    "demo": [], 
    "data": [
        "view/stock_move_entries_view.xml"
    ], 
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}