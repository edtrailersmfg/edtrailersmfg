# -*- encoding: utf-8 -*-

{
    "name" : "Conector con el PAC SIFEI",
    "version" : "1.0",
    "author" : "Fixdoo",
    "category" : "Localization/Mexico",
    "description" : """
    
    Conector con el PAC SIFEI
    
    www.sifei.com.mx
    
""",
    "website" : "http://www.fixdoo.mx",
    "depends" : [
                    "l10n_mx_einvoice",
                ],
    "data"    : [
                    'res_config_settings_view.xml',
                    'views/account_invoice_view.xml',
                    'views/account_payment_view.xml',
                ],
    "installable" : True,
    'license': 'Other proprietary',
}
