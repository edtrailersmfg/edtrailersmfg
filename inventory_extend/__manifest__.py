# -*- coding: utf-8 -*-
{
    'name' : 'Tipo de Cambio para Calcular Costo y Precio del Producto',
    'description':"""
            Inventory Extend
            =======================================
            Calculamos el Precio de Venta en MXN y USD de los productos a partir 
            del costo del producto y obteniendo el tipo de cambio más reciente
            en el sistema.
    """,
    'version' : '15.0.1',
    'category': 'Inventory/Inventory',
    'author': 'Enrique Jaquez',
    'depends' : [
        'account',
        'base',
        'product',
        'account_edi',
        'l10n_mx',
        'base_vat',
        'product_unspsc'        
        ],
    'data': [
        'views/product_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}