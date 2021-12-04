# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    cfdi_num_exportador_confiable = fields.Char(string="Número Exportador Confiable",
                                                related='company_id.cfdi_num_exportador_confiable', 
                                                readonly=False)