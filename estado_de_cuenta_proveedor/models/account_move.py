# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Integer(string="Días Vencidos", compute="_compute_dias", store=False)

    @api.depends('invoice_date_due','invoice_date')
    def _compute_dias(self):
        fecha_actual = datetime.now()
        for rec in self:
            if rec.invoice_date_due:
                fecha_limite = datetime.strptime(rec.invoice_date_due, "%Y-%m-%d")
                diferencia = fecha_actual - fecha_limite
                diferencia_en_dias = diferencia.days
                rec.dias = diferencia_en_dias
                #rec.dias = 1
            else:
                rec.dias = 0

