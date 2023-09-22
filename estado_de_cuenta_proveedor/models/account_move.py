# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Integer(string="Días Vencidos", compute="_compute_dias", store=True)

    @api.depends('invoice_date', 'invoice_date_due')
    def _compute_dias(self):
        now = datetime.now()
        for rec in self:
            rec.dias = (rec.invoice_date_due - now).days

