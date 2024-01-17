# -*- coding: utf-8 -*-
{
    'name' : 'Product Tracking App',
    'description':"""
Product Tracking App
======================================================
From Sale Order > Production > Inventory > To Customer
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
        'product_unspsc',
        'sale',
        'sale_management',
        'sale_stock',
        ],
    'data': [
        #'security/ir.model.access.csv',
        #'views/product_views.xml'
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