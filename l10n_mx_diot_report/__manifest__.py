# -*- encoding: utf-8 -*-


{
    "name" : "DIOT",
    "version" : "1.0",
    "author" : "Argil Consulting",
    "category" : "Localization/Mexico",
    "description": """
Declaración de Operaciones con Terceros (DIOT)
==============================================

- Se simplifica la definición de los datos requeridos por la DIOT
    + Se elimina la selección del País ya que se toma del país que tenga la dirección del Partner
- La Nacionalidad se captura en el país (abrir el registro del país y allí definir 'Nacionalidad')
- Al agregar un nuevo registro y dependiendo el país seleccionado en automático se 
   presupone el Tipo de Proveedor (04 - Nacional , 05 - Extranjero); pero se conserva la posibilidadç
   de usar un Proveedor Global (15)

    

    """,
    "website" : "http://www.argil.mx",

    "depends" : [
        "l10n_mx",
        "account_tax_cash_basis_argil"
        ],
    "data" : [
        "security/ir.model.access.csv",
        "data/account_tax_data.xml",
        "views/partner_view.xml",
        "views/product_view.xml",
        "views/account_move_view.xml",
        "views/res_country_view.xml",
        "wizard/wizard_diot_report_view.xml",
    ],
    'js': [],
    'qweb' : [],
    'css':[],
    'test': [],
    "installable" : True,
}
