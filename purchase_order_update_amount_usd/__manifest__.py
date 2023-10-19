# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'purchase_order_update_amount_usd',
    'author' : 'Enrique Jaquez',
    'version' : '15.0.1',
    'summary': 'Update Amount in USD and MXN in Purchase Order',
    'sequence': 10,
    'description': """
Update Amount in USD and MXN in Purchase Order
===============================
Update Amount in USD and MXN in Purchase Order depending of USD daily rate

Update Amount in USD and MXN in Purchase Order depending of USD daily rate
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com',
    'depends' : ['base','product','account','purchase','requisition'],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
