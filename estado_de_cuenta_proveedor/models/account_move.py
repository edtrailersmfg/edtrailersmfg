# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Integer(string="Días Vencidos", compute="_compute_dias", store=True)

    @api.depends('invoice_date', 'invoice_date_due')
    def _compute_dias(self):
        fmt = '%Y-%m-%d'
        for rec in self:
            rec.dias = 0
            start_date = self.invoice_date
            end_date = self.invoice_date_due
            d1 = datetime.strptime(start_date, fmt)
            d2 = datetime.strptime(end_date, fmt)
            rec.dias = (d2 - d1).days

