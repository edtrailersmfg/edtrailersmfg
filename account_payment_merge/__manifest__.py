# -*- encoding: utf-8 -*-

{
    "name"      : "Fusionar Pagos de Clientes previo CFDI",
    "version"   : "1.0",
    "author"    : "Fixdoo",
    "category"  : "Localization/Mexico",
    "description" : """
    
    Módulo que permite fusionar los Pagos confirmados para que posteriormente se pueda generar el CFDI correspondiente.
    
    """,
    "website" : "http://www.fixdoo.mx",
    'license': 'Other proprietary',
    "depends" : [
                "l10n_mx_einvoice",
    ],
    "data" : [
        'security/ir.model.access.csv',
        'wizard/account_payment_merge_view.xml',
             ],
    "installable" : True,
}
