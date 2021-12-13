
{
    "name"      : "Ejercicio Fiscal y Periodos Mensuales", 
    "version"   : "1.0", 
    'summary'   : 'Ejercicio Fiscal y Periodos Mensuales',
    'sequence'  : 20,
    "author"    : "Argil Consulting", 
    "category"  : "Account", 
    "description": """

Ejercicio Fiscal y Periodos Mensuales
=====================================

Aunque Odoo agregó el objeto Ejercicio Fiscal, por compatibilidad en la Locaización Mexicana de Argil se mantiene esta funcionalidad. 
      Este módulo agrega Ejercicio Fiscal y el Periodos Mensuales "dummy" para poder migrar el módulo de IFRS 
y otros reportes de Argil Consulting.

El Año Fiscal en México es prácticamente un año Natural.

Para México es necesario tener 13 periodOs, por ejemplo para el Año Fiscal 2019
se necesita:


Periodo => Periodo de Apertura

-  01/2019    =>   [   ]
-  02/2019    =>   [   ]
-  03/2019    =>   [   ]
-  04/2019    =>   [   ]
-  05/2019    =>   [   ]
-  06/2019    =>   [   ]
-  07/2019    =>   [   ]
-  08/2019    =>   [   ]
-  09/2019    =>   [   ]
-  10/2019    =>   [   ]
-  11/2019    =>   [   ]
-  12/2019    =>   [   ]
-  13/2019    =>   [ X ]

    """, 
    "website": "http://www.argil.mx", 
    #'license' : 'OEEL-1',
    "depends": [
        "account", 
    ], 

    "data": [
        'security/ir.model.access.csv',
        "views/account_view.xml",
            ], 
    "installable": True, 
    "post_init_hook": "post_init_hook",
}