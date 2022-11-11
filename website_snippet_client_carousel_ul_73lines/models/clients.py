# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Partner(models.Model):
    _inherit = ['res.partner']
    _name = 'res.partner'

    client_carousel_image = fields.Binary(string="Client Carousel Image",
                                          help="Display On Website "
                                               "Client Carousel.")
