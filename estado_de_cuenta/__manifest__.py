# -*- coding: utf-8 -*-
{
    "name": "Estado de Cuenta del Cliente",
    "summary": """
        Estado de Cuenta
        Reporte de Estado de Cuenta del Cliente
        Muestra el listado de Facturas Sin Pago y con Pago Parcial
    """,
    "version": "15.0.2",
    "category": "Account",
    "website": "https://www.sursoom.mx",
    "author": "Sursoom",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'base',
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
