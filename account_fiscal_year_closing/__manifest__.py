
{
    "name": "Póliza de Cierre de Año Fiscal", 
    "version": "1.0", 
    "author": "Argil Consulting", 
    "category": "Account", 
    "description": """

Póliza de Cierre de Año Fiscal
==============================

Este módulo ayuda para generar la Póliza de Cierre de Año Fiscal (Póliza de Resultados)
- Agrega el Asistente para crear la Póliza de Resultados
- Agrega el Asistente para Cerrar el Año Fiscal

    """, 
    "website": "http://www.argil.mx", 
    #'license' : 'OEEL-1',
    "depends": ["account", 
                "account_period_and_fiscalyear",], 
    "demo": [], 
    "data": [
        'security/ir.model.access.csv',
        'account_view.xml',
    ], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}