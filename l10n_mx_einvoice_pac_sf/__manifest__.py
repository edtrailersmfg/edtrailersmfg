# -*- encoding: utf-8 -*-

{
    "name" : "Conector con el PAC Solución Factible",
    "version" : "1.0",
    "author" : "Argil Consulting",
    "category" : "Localization/Mexico",
    "description" : """
    
    Este m&oacute; es el conector con el PAC Soluci&oacute;n Factible. 
    
    www.solucionfactible.com
    
    
""",

    "website" : "http://www.argil.mx",
    "depends" : [
                "l10n_mx_einvoice",
                ],
    "data" : [
                'views/account_invoice_view.xml',
                'views/account_payment_view.xml',
            ],
    "installable" : True,
}
