# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ReportInvoiceWithPayment(models.AbstractModel):
    _name = 'report.estado_de_cuenta.report_account_report'
    _description = 'Estado de Cuenta'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.report.wizard.customer'].browse(docids)
        move_data = docs._get_move_data_report_values()
        return {
            'doc_ids': docids,
            'doc_model': 'account.report.wizard.customer',
            'docs': docs,
            'move_data': move_data,
        }
