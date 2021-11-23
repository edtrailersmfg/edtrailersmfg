# -*- encoding: utf-8 -*-
## Hecho por German Ponce Dominguez - german.ponce@outlook.com ##

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class ResCompany(models.Model):
    _name = 'res.company'
    _inherit ='res.company'

    odoo_serial_key = fields.Char('No. Licencia', copy=False, readonly=False)

