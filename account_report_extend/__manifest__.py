# -*- coding: utf-8 -*-
{
    "name": "Account Report Extend",
    "summary": """
        Account Report Extend
        Reporte de Facturación
    """,
    "version": "15.0.1.0.0",
    "category": "Account",
    "website": "https://www.sursoom.mx",
    "author": "Sursoom",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'account',
        'report_xlsx'
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/account_report_wizard_views.xml',
        'report/account_report_template_views.xml',
        'report/account_report.xml',
        'views/account_move_views.xml'
    ],
}
