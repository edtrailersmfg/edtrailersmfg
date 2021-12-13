# -*- encoding: utf-8 -*-
{
    "name"      : "Facturación Electrónica para México",
    "version"   : "1.0",
    "Summary"   : "Facturación Electrónica para México",
    "sequence"  : 50,
    "author"    : "Argil Consulting",
    "category"  : "Localization",
    "description" : """
Facturación Electrónica México
==============================


Este módulo extiende Odoo para poder manejar Facturación Electrónica de acuerdo a los requerimientos del SAT

* Factura Electrónica (Facturas y Notas de Crédito)

* Manejo de Anticipos en Factura Electrónica (Identificando cuáles ya fueron aplicados)

* CFDI Recibo Electrónico de Pagos

* Diversos Complementos
    - Comercio Exterior
    - Detallista
    - Pago de terceros
    - Complemento de Escuelas (Colegiaturas)
    - Etc.
    

    """,
    "website" : "http://www.argil.mx",
    "depends" : ["account",
                 #"account_cancel", - Modulo descontinuado por Odoo
                 "base_vat",
                 "base_address_extended",
                 "product",
                 #"stock_account",
                 "uom",
                 'attachment_indexation',
                 #"email_template_multicompany",
                ],
    "data" : [
                'security/ir.model.access.csv',
                'data/data.xml', # Catalogos Pequeños pero Requeridos
                'data/sat.tipo.relacion.cfdi.csv', # Tipos de Relacion entre CFDI
                'data/sat.regimen.fiscal.csv', # Regimen Fiscales Actualizados
                'data/payment_method_data.xml', # Metodos de pago
                'data/country_data_address.xml', # Formato de direccion
                'data/sat.regimen.fiscal.csv', # Regimen Fiscales Actualizados
                'data/sat.udm.csv', # Unidades de Medida
                'data/sat.aduana.csv', # Aduanas
                'data/res.country.township.sat.code.csv', # Municipios
                'data/res.country.locality.sat.code.csv', # Localidades
                
                'views/menu_view.xml',
                'views/res_partner_view.xml',
                'views/account_tax_view.xml',
                'views/product_view.xml',
                'views/res_company_view.xml',
                'views/catalogos_sat_view.xml',
                'wizard/sat_catalogos_wizard_view.xml',
                # 'wizard/upload_data_view.xml', # Ya no se usa
                'views/account_journal_view.xml',
                
                
                'views/account_payment_term_view.xml',
                'views/res_config_settings_view.xml',
                'views/res_partner_bank_view.xml',
                'views/account_move_view.xml',
                'views/account_payment_view.xml',
                'report/l10n_mx_einvoice_payment_report.xml',
                'data/payment_mail_template.xml',
                'report/l10n_mx_einvoice_invoice_report.xml',
                

    ],
    "post_init_hook": "post_init_hook",
    'installable'   : True,
    'application'   : True,

    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: