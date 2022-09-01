# -*- coding: utf-8 -*-
from odoo import models, _
PAYMENT_STATE = {
    'not_paid': 'Sin Pagar',
    'in_payment': 'En Proceso de Pago',
    'paid': 'Pagado',
    'partial': 'Pagado Parcialmente',
    'reversed': 'Revertido',
    'invoicing_legacy': 'Sistema anterior de Facturación',
}

class AccountReportXlsx(models.AbstractModel):
    _name = "report.account_report_extend.report_account_report_excel"
    _inherit = "report.report_xlsx.abstract"
    _description = "Reporte de Facturación"

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Reporte Facturas")
        i = 0
        j = 0

        TABLE_HEADER = [
            _('Fecha Factura'),
            _('Factura #'),
            _('Cliente'),
            #_('RFC'),
            #_('Folio Fiscal'),
            #_('Precio Venta'),
            #_('Descuento'),
            #_('Impuesto'),
            _('Total con Signo'),
            _('Importe'),
            _('Costo'),
            _('Beneficio'),
            _('Margen %'),
            _('Estado del Pago')
        ]

        move_data = wizard._get_move_data_report_values()
        bold = workbook.add_format({"bold": True})

        for table in TABLE_HEADER:
            sheet.write(i, j, table, bold)
            j += 1

        for m in move_data:
            i += 1
            j = 0
            sheet.write(i, j, str(m.invoice_date), '')
            j += 1
            sheet.write(i, j, m.name or '', '')
            j += 1
            sheet.write(i, j, str(m.partner_id.name), '')
            j += 1
            #sheet.write(i, j, str(m.partner_id.vat), '')
            #j += 1
            #sheet.write(i, j, str(m.l10n_mx_edi_cfdi_uuid), '')
            #j += 1
            #sheet.write(i, j, m.price, '')
            #j += 1
            #sheet.write(i, j, m.discount, '')
            #j += 1
            #sheet.write(i, j, m.amount_tax, '')
            #j += 1
            sheet.write(i, j, m.amount_untaxed_signed, '')
            j += 1
            sheet.write(i, j, m.amount_untaxed, '')
            j += 1
            sheet.write(i, j, m.cost_amount, '')
            j += 1
            sheet.write(i, j, m.profit, '')
            j += 1
            sheet.write(i, j, m.margin, '')
            j += 1
            sheet.write(i, j, PAYMENT_STATE[m.payment_state], '')
            j += 1
