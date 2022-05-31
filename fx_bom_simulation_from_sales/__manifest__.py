# -*- coding: utf-8 -*-
{
    'name': 'Simulación de materiales',
    "category" : "Manufacture",
    'description': """
        El módulo agrega una acción de servidor al modelo de ventas, la cual genera una simulación
        de la explosión de una lista de materiales para las partidas en los pedidos.
        Posteriormente las presenta en una vista de lista para su revisión.
        Estos registros nuevos tienen una acción de servidor que permite generar órdenes de compra
        a partir de ellos.
    """,
    'author': 'Rene Vera Apale',
    'website': '',
    "support": "",
    'version': '15.0.0.1.0',
    "license" : "AGPL-3",
    "depends" : ["sale","mrp"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
                    'security/ir.model.access.csv',
                    'data/requirement_simulation_action.xml',
                    'data/sale_order_server_action.xml',
                    'views/requirement_simulation_views.xml',
                    ],
    "installable" : True,
    "active" : False,
}
