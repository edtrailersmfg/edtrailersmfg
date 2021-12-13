# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

{
    'name' : 'Contabilidad Electrónica para México',
    'description' : """
    Adecuación para cumplir con los requisitos de la Contabilidad Electrónica
         promulgada en 2014. Este módulo añade puntos específicos requeridos para generar los documentos
         XML requeridos por SAT.
         """,
    'version': '1.0',
    'author' : 'Argil',
    'website': 'http://www.argil.mx',
    #'license' : 'OEEL-1',
    'category' : 'Accounting',
    'depends' : ['base', 
                 'account',
                 'argil_mx_accounting_reports_consol', 
                 'l10n_mx_einvoice',
                 'l10n_mx_diot_report'
                ],
    'data'  : [

              'data/ir_config_parameter.xml',
               'data/complements.xml',
               'security/ir.model.access.csv',
               'views/res_company_view.xml',
               'views/account_journal_view.xml',
               'views/account_view.xml',
               'views/eaccount_account_bank_view.xml',
               'views/account_move_view.xml',
               'views/account_moveline_view.xml',
               'views/hesa_filegenerate_view.xml',
               'views/restrictive_actions.xml',
               'views/account_invoice_view.xml',
               'views/account_payment_view.xml',
               'wizard/files_generator_view.xml',
               'wizard/movelines_info_manager_view.xml',
               'wizard/xsdvalidation_handler_view.xml',
               'report/report_catalogo_cuentas.xml',
               'report/report_balanza_mensual.xml',
               'views/menu.xml',
              ],
    'installable' : True,
}
# Revision: 3.0
# Release: 1.0
