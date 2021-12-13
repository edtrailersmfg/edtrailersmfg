# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = 'res.company'

    
    pac     = fields.Selection(selection_add=[('pac_sifei', 'SIFEI - https://www.sifei.com.mx'),], 
                               string="PAC", ondelete={'pac_sifei': 'set null'})
    
    pac_equipo_id = fields.Char(string="Equipo ID", help="Este dato lo entrega el PAC")
    
    pac_user_4_testing      = fields.Char(string="Usuario ")
    pac_password_4_testing  = fields.Char(string="Contraseña ")
    pac_equipo_id_4_testing = fields.Char(string="Equipo ID ", help="Este dato lo entrega el PAC")