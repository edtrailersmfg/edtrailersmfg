import pytz
from openerp import models, fields, api, _
from datetime import timedelta, datetime
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class AccounutReportWizard(models.TransientModel):
    _name = "account.report.wizard"
    _description = "Estado de Cuenta del Proveedor"

    supplier = fields.Many2one('res.partner', string="Proveedor", domain="[('supplier_rank', '>', 0)]")
    start_date = fields.Datetime(string="Fecha Inicial : ", default=lambda self: fields.datetime.now())
    end_date = fields.Datetime(string="Fecha Final : ", default=lambda self: fields.datetime.now())

    def action_get_report_values(self):
        return self.env.ref('estado_de_cuenta_proveedor.action_report_account_report').report_action(self)

    def action_get_xlsx_report(self):
        return self.env.ref('estado_de_cuenta_proveedor.action_report_account_report_xlsx').report_action(self)

    def _get_move_data_report_values(self):
        docs = self
        AccountMove = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '!=', 'paid'),
            ('payment_state', '!=', 'in_payment'),
            ('payment_state', '!=', 'reversed'),
            ('currency_id', '=', 'USD'),
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
            ('payment_state', '!=', 'paid'),
            ('payment_state', '!=', 'in_payment'),
            ('payment_state', '!=', 'reversed'),
            ('currency_id', '=', 'MXN'),
        ]
        if docs.customer:
            domain.append(
                ('partner_id', '=', docs.customer.id),
            )
        move_ids = AccountMove.search(domain)
        return move_ids

