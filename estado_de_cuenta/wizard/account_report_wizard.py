import pytz
from openerp import models, fields, api, _
from datetime import timedelta, datetime
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class AccounutReportWizard(models.TransientModel):
    _name = "account.report.wizard"
    _description = "Estado de Cuenta"

    customer = fields.Many2one('res.partner', string="Cliente : ")
    start_date = fields.Datetime(string="Fecha Inicial : ", default=lambda self: fields.datetime.now())
    end_date = fields.Datetime(string="Fecha Final : ", default=lambda self: fields.datetime.now())
    sin_pagar = fields.Boolean(string="Mostrar solo pendientes de pago", default=False)

    def action_get_report_values(self):
        return self.env.ref('estado_de_cuenta.action_report_account_report').report_action(self)

    def action_get_xlsx_report(self):
        return self.env.ref('estado_de_cuenta.action_report_account_report_xlsx').report_action(self)

    def _get_move_data_report_values(self):
        docs = self
        AccountMove = self.env['account.move']
        if (self.sin_pagar == True):
            domain = [
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '!=', 'paid'),
                ('payment_state', '!=', 'reversed'),
                ('payment_state', '!=', 'in_payment'),
                ('currency_id', '=', 'USD'),
                ('invoice_date', '>=', self.start_date),
                ('invoice_date', '<=', self.end_date),            
            ]
        else:
            domain = [
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice'),
                ('currency_id', '=', 'USD'),
                ('invoice_date', '>=', self.start_date),
                ('invoice_date', '<=', self.end_date),            
            ]            
        if docs.customer:
            domain.append(
                ('partner_id', '=', docs.customer.id),
            )
        move_ids = AccountMove.search(domain)
        return move_ids

    def _get_move_data_report_values2(self):
        docs = self
        AccountMove = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('currency_id', '=', 'MXN'),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),            
        ]
        if docs.customer:
            domain.append(
                ('partner_id', '=', docs.customer.id),
            )
        move_ids = AccountMove.search(domain)
        return move_ids


