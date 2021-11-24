# -*- encoding: utf-8 -*-

{
    "name": "Reclasificación de Impuesto Efectivamente Cobrado/Pagado", 
    "version": "1.0", 
    "author": "Argil Consulting", 
    "category": "Localization/Mexico", 
    "description": """

Impuesto efectivamente Pagado/Cobrado al momento del Pago
=========================================================

Este m&oacute;dulo agrega la funcionalidad de agregar las partidas contables de
reclasificaci&oacute; de impuesto efectivamente pagado/cobrado en la p&oacute;liza del
pago/cobro.

Depender&aacute; de la configuraci&oacute; del impuesto.

    """, 
    "website": "http://www.argil.mx", 
    #'license' : 'OEEL-1',
    "depends": [
        "account", 
        #"account_invoice_payment_by_date_due", 
        #"l10n_mx_einvoice",
        #"l10n_mx_diot_report",
    ], 
    "demo": [], 
    "data": [
        #"views/account_tax_view.xml",
        #"views/account_move_view.xml",
            ], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
    #"auto_install": False, 
    #"active": False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: