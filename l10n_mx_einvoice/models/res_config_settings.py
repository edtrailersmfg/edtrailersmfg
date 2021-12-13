# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pac         = fields.Selection(string="PAC", related='company_id.pac', readonly=False)
    pac_user    = fields.Char(string="Usuario", related='company_id.pac_user', readonly=False)
    pac_password= fields.Char(string="Contraseña", related='company_id.pac_password', readonly=False)
    pac_testing = fields.Boolean(string="Pruebas", related='company_id.pac_testing', readonly=False)
    validate_schema = fields.Boolean(string="Validar Esquema XSD de los XMLs de manera local", 
                                     related='company_id.validate_schema', readonly=False)

    regimen_fiscal_id = fields.Many2one('sat.regimen.fiscal', 
                                        related="company_id.regimen_fiscal_id", readonly=False)