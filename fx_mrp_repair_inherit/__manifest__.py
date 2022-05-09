# -*- coding: utf-8 -*-
{
    'name' : 'MRP Repair Inherit',
    'version' : '1.0',
    'summary': 'Personalización del módulo nativo MRP Repair',
    'sequence': 30,
    'description': """
    El módulo modifica el proceso del módulo de reparaciones para generar registros de stock.picking
    junto con el stock.move creado nativamente. Se agrega un catálogo de motivos de reparación y se
    relaciona el pedido de venta y el stock.picking con la reparación.
    """,
    'category': 'MRP',
    'website': '',
    'images' : [],
    'depends' : ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_repair_causes_views.xml'
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
