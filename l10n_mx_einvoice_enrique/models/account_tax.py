# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError


class AccountTax(models.Model):
    _inherit ='account.tax'

    sat_tasa_cuota = fields.Selection([('Tasa','Tasa'),
                                       ('Cuota','Cuota'),
                                       ('Exento','Exento'),], 'Tasa o Cuota')
    
    sat_code_tax = fields.Selection([('001','[ 001 ] ISR'),
                                     ('002','[ 002 ] IVA'),
                                     ('003','[ 003 ] IEPS'),
                                     ('004','[ 004 ] Impuesto Local')], 'Clave SAT')

    local_tax = fields.Char('Impuesto Local')
