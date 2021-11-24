
{
    "name": "Moneda en Facturas", 
    "version": "1.0", 
    "author": "Argil Consulting", 
    "category": "Account", 
    "description": """

Moneda en Facturas
==================

Este módulo agrega en el listado de Facturas el filtro y agrupación por Moneda.

Además de que agrega un campo para capturar Moneda Extranjera como (ejemplo para USD):
1/T.C. Actual: 24.2442
Tasa: 0.041246978658813


Si ya tiene tiempo usando Odoo es recomendable correr el siguiente script para actualizar lo histórico

update res_currency_rate set rate2=1/rate where rate <> 0;

    """, 
    "website": "http://www.argil.mx", 
    #'license' : 'OEEL-1',
    "depends": [
        "account", 
    ], 
    "demo": [], 
    "data": ["views/account_move_view.xml",
             "views/res_currency_view.xml",
            ], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}