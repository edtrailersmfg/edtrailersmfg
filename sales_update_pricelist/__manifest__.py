# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'sales_update_pricelist',
    'author' : 'Enrique Jaquez',
    'version' : '15.0.1',
    'summary': 'Update Pricelist with Cost USD, Profit, Margin % and Cost MXN',
    'sequence': 10,
    'description': """
ED Trailers Pricelist
====================
Update Pricelist with Cost USD, Profit, Margin % and Cost MXN

Update Pricelist with Cost USD, Profit, Margin % and Cost MXN
    """,
    'category': 'Sales/Sales',
    'website': 'https://www.odoo.com',
    'depends' : ['base','sale_management'],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
