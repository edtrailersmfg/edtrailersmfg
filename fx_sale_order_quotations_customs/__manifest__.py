# -*- coding: utf-8 -*-
# Coded by German Ponce Dominguez 
#     ▬▬▬▬▬.◙.▬▬▬▬▬  
#       ▂▄▄▓▄▄▂  
#    ◢◤█▀▀████▄▄▄▄▄▄ ◢◤  
#    █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬  
#    ◥ █████ ◤  
#     ══╩══╩═  
#       ╬═╬  
#       ╬═╬ Dream big and start with something small!!!  
#       ╬═╬  
#       ╬═╬ You can do it!  
#       ╬═╬   Let's go...
#    ☻/ ╬═╬   
#   /▌  ╬═╬   
#   / \
# Cherman Seingalt - german.ponce@outlook.com
{
    'name': 'Modificaciones Tarifas y Cotizaciones',
    "category" : "Sales",
    'description': """

        Este modulo nos permite modificar las tarifas o listas de precios y realizar cotizaciones avanzadas.

    """,
    'author': 'German Ponce Dominguez',
    'website': 'http://fixdoo.mx',
    "support": "german.ponce@outlook.com",
    'version': '15.0.0.1.0',
    "license" : "AGPL-3",
    "depends" : [
                    "account",
                    "sale",
                    "sales_team",
                ],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
                    'security/ir.model.access.csv',
                    'sale_view.xml',
                    ],
    "installable" : True,
    "active" : False,
}
