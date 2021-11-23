# -*- coding: utf-8 -*-
##############################################################################
#
#   Original by Odoo SA
#   Forked by:
#   2016 - Fixdoo SA de CV
#    (<http://www.fixdoo.mx>)
##############################################################################
{
    'name': "Account Move Subcription",
    'version': '1.0',
    'category': 'Account',
    'summary': "Templates for recurring Journal Entries",
    'author': "Fixdoo,Odoo SA",
    'website': 'http://www.fixdoo.mx',
    'depends': ['account', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'view/account_subscription_view.xml',
        'wizard/account_subscription_wizard_view.xml',
    ],
    'test': [],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: