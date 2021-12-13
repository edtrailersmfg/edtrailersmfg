# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = 'res.company'

    
    pac     = fields.Selection(selection_add=[('pac_sf', 'Solución Factible - https://www.solucionfactible.com'),], 
                                       string="PAC", ondelete={'pac_sf': 'set null'})
    
