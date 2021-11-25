# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging
_logger = logging.getLogger(__name__)

class SAT_CatalogosWizard(models.TransientModel):
    _name = 'sat.catalogos.wizard'
    _description ="Catalogos del SAT para CFDI 3.3 y Contabilidad Electronica"

    catalogo = fields.Selection([('action_sat_tipo_comprobante', 'Tipos de Comprobantes'),
                                 ('action_sat_uso_cfdi', 'Uso de CFDI'),
                                 ('action_sat_tipo_relacion_cfdi', 'Tipos de Relación de CFDIs'),
                                 ('action_sat_regimen_fiscal', 'Régimen Fiscal'),
                                 ('action_sat_formas_pago', 'Formas de Pago (CFDI Facturas)'),
                                 ('action_sat_metodo_pago', 'Métodos de Pago (CFDI Facturas)'),
                                 ('action_sat_producto', 'Productos y Servicios'),
                                 ('action_sat_udm', 'Unidades de Medida'),
                                 ('action_sat_impuesto', 'Impuestos'),
                                 ('action_sat_arancel', 'Fracciones Arancelarias'),
                                 ('action_sat_country_township_codes', 'Municipios'),
                                 ('action_sat_country_locality_codes', 'Localidades'),
                                 ('action_sat_country_zip_codes', 'Códigos Postales'),
                                 ('action_sat_colonia_zip_codes', 'Colonias'),
                                 ('action_sat_aduana_codes', 'Aduanas'),
                                 ('action_eaccount_banks', 'Bancos'),
                                 ('action_sat_moneda', 'Monedas'),
                                 ('sat_accountcode_action', 'Agrupadores de Cuentas (Contabilidad Electrónica)'),
                                 ('eaccount_payments_action', 'Métodos de Pago (Contabilidad Electrónica)'),                                 
                                ],
                               string="Catálogo", required=True)
    

    
    def open_catalog(self):
        #_logger.info("self.catalogo: %s" % self.catalogo)
        modelos = {
            'action_sat_tipo_comprobante': 'sat.tipo.comprobante',
            'action_sat_uso_cfdi': 'sat.uso.cfdi',
            'action_sat_tipo_relacion_cfdi': 'sat.tipo.relacion.cfdi',
            'action_sat_regimen_fiscal': 'regimen.fiscal',
            'action_sat_formas_pago': 'pay.method',
            'action_sat_metodo_pago': 'sat.metodo.pago',
            'action_sat_producto': 'sat.producto',
            'action_sat_udm': 'sat.udm',
            'action_sat_impuesto': 'sat.impuesto',
            'action_sat_arancel': 'sat.arancel',
            'action_sat_country_township_codes': 'res.country.township.sat.code',
            'action_sat_country_locality_codes': 'res.country.locality.sat.code',
            'action_sat_country_zip_codes': 'res.country.zip.sat.code',
            'action_sat_colonia_zip_codes': 'res.colonia.zip.sat.code',
            'action_sat_aduana_codes': 'sat.aduana',
            'action_eaccount_banks': 'eaccount.bank',
            'action_sat_moneda': 'eaccount.currency',
            'sat_accountcode_action': 'sat.account.code',
            'eaccount_payments_action': 'eaccount.payment.methods',
        }
        
        catalogos = dict(self._fields['catalogo'].selection)
        
        return {
            'name': _('%s') % catalogos[self.catalogo],
            'res_model': modelos[self.catalogo],
            'view_mode': 'tree',
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: