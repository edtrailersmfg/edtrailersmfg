# -*- coding: utf-8 -*-
{
    'name': "Cantidad de Producto en Almacén",
    'author': 'Enrique Jaquez',
    'category': 'Warehouse',
    'summary': """Muestra los productos disponibles por almacén, lo muestra en la vista kanban y form en el producto""",
    'license': 'AGPL-3',
    'website': '',
    'description': """
""",
    'version': '15.0.1',
    'depends': ['sale','stock'],
    'data': ['security/warehouse_security.xml','views/product_view.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
