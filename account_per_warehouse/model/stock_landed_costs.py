# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero
import logging
_logger = logging.getLogger(__name__)

class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'
    
    
    def _create_accounting_entries(self, move, qty_out):
        # TDE CLEANME: product chosen for computation ?
        cost_product = self.cost_line_id.product_id
        if not cost_product:
            return False
        accounts = self.product_id.product_tmpl_id.get_product_accounts()
        debit_account_id = accounts.get('stock_valuation') and accounts['stock_valuation'].id or False
        ### Inicio ARGIL
        data = self.cost_line_id.cost_id.picking_ids[0].show_entry_lines()
        if data and data.get('domain', False) and len(data['domain'][0][2]) > 0:
            ml_ids = data['domain'][0][2]
            for ml in self.env['account.move.line'].browse(ml_ids):
                if ml.debit:
                    debit_account_id = ml.account_id.id
                    break        
        ### Fin ARGIL
        # If the stock move is dropshipped move we need to get the cost account instead the stock valuation account
        if self.move_id._is_dropshipped():
            debit_account_id = accounts.get('expense') and accounts['expense'].id or False
        already_out_account_id = accounts['stock_output'].id
        credit_account_id = self.cost_line_id.account_id.id or cost_product.categ_id.property_stock_account_input_categ_id.id

        if not credit_account_id:
            raise UserError(_('Please configure Stock Expense Account for product: %s.') % (cost_product.name))

        return self._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)