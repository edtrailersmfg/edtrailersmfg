# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Char(string="Días Vencidos", compute="_compute_dias", store=True)

    @api.depends('invoice_date', 'invoice_date_due')
    def _compute_dias(self):
        for rec in self:
            rec.dias = (rec.invoice_date_due - rec.invoice_date).days

