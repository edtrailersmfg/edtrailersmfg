# -*- encoding: utf-8 -*-

{
    "name" : "Conector con el PAC SIFEI con LM de Odoo EE",
    "version" : "1.0",
    "author" : "Argil Consulting",
    "category" : "Localization/Mexico",
    "description" : """
    
    Conector con el PAC SIFEI para Odoo EE
    
    www.sifei.com.mx
    
""",
    "website" : "http://www.argil.mx",
    "depends" : [
                    "l10n_mx_edi",
                ],
    "data"    : [
        'views/res_config_settings_view.xml',
        'views/l10n_mx_edi_certificate_view.xml'
    ],
    "installable" : True,
}
