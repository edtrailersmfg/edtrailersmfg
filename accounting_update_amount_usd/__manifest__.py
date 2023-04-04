# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'accounting_update_amount_usd',
    'author' : 'Enrique Jaquez',
    'version' : '15.0.1',
    'summary': 'Update Amount in USD and MXN in Accounting',
    'sequence': 10,
    'description': """
Update Amount in USD and MXN in Accounting
===============================
Update Amount in USD and MXN in Accounting depending of USD daily rate

Update Amount in USD and MXN in Accounting depending of USD daily rate
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com',
    'depends' : ['base','product','account'],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
