# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
import time
import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    cfdi_num_exportador_confiable = fields.Char(string="Número Exportador Confiable")