# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    import_ids = fields.Many2many('import.info', 'account_invoice_line_import_info_rel', 'invoice_line_id', 'import_id',
                                        string='Pedimentos')


class import_info(models.Model):
    _inherit = "import.info"    
    
    invoice_line_ids = fields.Many2many('account.move.line', 'account_invoice_line_import_info_rel', 'import_id', 'invoice_line_id',
                                         string='Líneas de Factura')

