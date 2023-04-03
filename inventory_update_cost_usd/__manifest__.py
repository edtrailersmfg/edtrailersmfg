# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'inventory_update_cost_usd',
    'author' : 'Enrique Jaquez',
    'version' : '15.0.1',
    'summary': 'Update Cost in USD in inventory',
    'sequence': 10,
    'description': """
Update Cost in USD in inventory
===============================
Update Cost in USD in inventory depending of USD daily rate

Update Cost in USD in inventory depending of USD daily rate
    """,
    'category': 'Inventory/Inventory',
    'website': 'https://www.odoo.com',
    'depends' : ['base','product'],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
