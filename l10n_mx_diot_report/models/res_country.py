# -*- coding: utf-8 -*-
#
from odoo import api, fields, models, _, tools

class ResCountry(models.Model):

    _inherit = 'res.country'

    nacionality      = fields.Char('Nacionalidad', help="Ayuda a definir como se le nombra a las personas de este País")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
