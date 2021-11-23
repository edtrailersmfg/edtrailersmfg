# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'    

    pac_equipo_id = fields.Char(related='company_id.pac_equipo_id',
                                readonly=False)
    pac_user_4_testing      = fields.Char(related='company_id.pac_user_4_testing', readonly=False)
    pac_password_4_testing  = fields.Char(related='company_id.pac_password_4_testing', readonly=False)
    pac_equipo_id_4_testing = fields.Char(
                                          related='company_id.pac_equipo_id_4_testing',
                                          readonly=False)