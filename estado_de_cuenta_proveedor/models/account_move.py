# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    dias = fields.Integer(string="Días Vencidos", compute="_compute_dias", store=False)

    @api.depends('invoice_date_due','invoice_date')
    def _compute_dias(self):
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        fecha_dt = datetime.strptime(fecha_actual, '%Y-%m-%d')
        for rec in self:
            if rec.invoice_date_due:
                #fecha_limite = datetime.strptime(rec.invoice_date_due, "%Y-%m-%d")
                fecha_limite = rec.invoice_date_due
                fecha_dt2 = datetime(fecha_limite.year, fecha_limite.month, fecha_limite.day)
                #raise UserError("Fecha límite %s" %tipo_fecha_limite)
                diferencia_dt = fecha_dt - fecha_dt2
                diferencia_str = datetime.strptime(diferencia_dt, '%d')
                raise UserError("diferencia %s" %diferencia_str)
                #diferencia_en_dias = diferencia.days
                #rec.dias = diferencia_en_dias
                rec.dias = 1
            else:
                rec.dias = 0

