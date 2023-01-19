import pytz
from odoo import models, fields, api, _
from datetime import timedelta, datetime


class AccounutReportWizard(models.TransientModel):
    _name = "account.report.wizard"
    _description = "Reporte de Facturación"

    start_date = fields.Date(string="Fecha Inicial : ", required=True)
    end_date = fields.Date(string="Fecha Final : ", required=True)

    def action_get_report_values(self):
        return self.env.ref('account_report_extend.action_report_account_report').report_action(self)

    def action_get_xlsx_report(self):
        return self.env.ref('account_report_extend.action_report_account_report_xlsx').report_action(self)

    def _get_move_data_report_values(self):
        docs = self
        AccountMove = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
        ]
        if docs.start_date:
            domain.append(
                ('invoice_date', '>=', docs.start_date),
            )
        if docs.end_date:
            domain.append(
                ('invoice_date', '<=', docs.end_date),
            )
        move_ids = AccountMove.search(domain)
        return move_ids
