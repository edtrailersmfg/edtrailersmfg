# -*- encoding: utf-8 -*-

{
    "name" : "PAC SIFEI con LM de Odoo EE",
    "version" : "1.0",
    "author" : "Fixdoo",
    "category" : "Localization/Mexico",
    "description" : """
    
    Conector con el PAC SIFEI para Odoo EE
    
    www.sifei.com.mx
    
""",
    "website" : "http://www.fixdoo.mx",
    "depends" : [
        "account",
        "l10n_mx_edi",
                ],
    "data"    : [
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'views/l10n_mx_edi_certificate_view.xml',
        'wizard/account_cfdi_cancel_sat_view.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
    ],
    "installable" : True,
    'license': 'Other proprietary',
}
