# -*- encoding: utf-8 -*-
## Hecho por German Ponce Dominguez - german.ponce@outlook.com ##

{
    "name": "No. de Licencia en Aplicaciones Propias", 
    "version": "1.1", 
    "author": "German Ponce Dominguez", 
    "category": "Seguridad", 
    "description": """

    """, 
    "website": "http://poncesoft.blogspot.com", 
    "license": "AGPL-3", 
    "depends": [
                'base',
            ], 
    "external_dependencies":  {'python': ['cryptography','requests']},
    "data": [
            'application_view.xml',
    ], 
    "installable": True, 
    "auto_install": False, 
}