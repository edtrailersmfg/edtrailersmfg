# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Integer(string="Días Vencidos", compute="_compute_dias", store=False)

    @api.depends('invoice_date_due','invoice_date')
    def _compute_dias(self):
        now = (datetime.now()).strftime('%d/%m/%Y')
        for rec in self:
            if rec.invoice_date_due:
                rec.dias = (rec.invoice_date_due - now).days
                #rec.dias = 1
            else:
                rec.dias = 0

