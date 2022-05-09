# -*- coding:utf-8 -*-
from odoo import fields, models, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    invoice_method = fields.Selection(states={}, readonly=False)
    invoice_id = fields.Many2one(readonly=False)
    fees_lines = fields.One2many(readonly=False)