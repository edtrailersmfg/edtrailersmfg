# -*- coding: utf-8 -*-
#

from odoo import api, fields, models, _, tools

class ResPartner(models.Model):

    _inherit = 'res.partner'

    type_of_third   = fields.Selection([('04', ' 04 - Proveedor Nacional'),
                                        ('05', ' 05 - Proveedor Extranjero'),
                                        ('15', ' 15 - Proveedor Global')],
                                        string='Tipo de Proveedor')
    type_of_operation = fields.Selection([('03', ' 03 - Provision de Servicios Profesionales'),
                                          ('06', ' 06 - Arrendamientos'),
                                          ('85', ' 85 - Otros')],
                                            string='Tipo de Operación')
    
    number_fiscal_id_diot = fields.Char(string='Identificador Fiscal', size=100)
    
    
    @api.onchange('country_id')
    def _onchange_country_id(self):
        super(ResPartner, self)._onchange_country_id()
        if self.country_id.code=='MX':
            self.type_of_third = '04'
        else:
            self.type_of_third = '05'
        if not self.type_of_operation:
            self.type_of_operation='85'
            
        if 'num_reg_trib' in self._fields and self.num_reg_trib:
            self.number_fiscal_id_diot = self.num_reg_trib
            
            
    
        
            
        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
