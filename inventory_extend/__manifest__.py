# -*- coding: utf-8 -*-
{
    'name' : 'Tipo de Cambio para Calcular Costo y Precio del Producto',
    'description':"""
Inventory Extend
=======================================
Tipo de Cambio para Calcular Costo y Precio del Producto
    """,
    'version' : '15.0.1',
    'category': 'Inventory/Inventory',
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
        #'security/ir.model.access.csv',
        'views/product_views.xml'
        #'views/account_move_views.xml',
        #'views/account_payment_views.xml',
        #'views/account_journal_views.xml',
        #'data/cron.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}