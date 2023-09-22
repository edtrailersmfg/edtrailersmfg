# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Char(string="Días Vencidos", compute="_compute_dias", store=True)

    @api.depends('invoice_date', 'invoice_date_due')
    def _compute_dias(self):
        now = datetime.now()
        for rec in self:
            f1_str = now.strftime('%d/%m/%Y')
            rec.dias = f1_str

