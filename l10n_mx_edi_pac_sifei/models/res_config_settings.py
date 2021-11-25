# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'    

    l10n_mx_edi_pac_equipo_id = fields.Char(related='company_id.l10n_mx_edi_pac_equipo_id',
                                readonly=False)
