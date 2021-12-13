# -*- coding: utf-8 -*-

{
    "name"      : "Complemento Comercio Exterior 1.1",
    "version"   : "1.0",
    "author"    : "Argil Consulting",
    "website"   : "https://www.argil.mx",
    "category"  : "Localization/Mexico",
    "description": """

Complemento Comercio Exterior 1.1
=================================

Este modulo permite incorporar el Complemento de Comercio Exterior 1.1
obligatorio a partir del 1º Marzo 2018

""",
    "depends"   : ["account",
                   "sale_stock",
                   "l10n_mx_einvoice",
                  ],
    "data"      : [
        "views/res_config_settings_view.xml",
        "views/product_template_view.xml",
        "views/account_move_view.xml",
        "views/res_partner.xml",
                  ],
    "installable": True,
}
