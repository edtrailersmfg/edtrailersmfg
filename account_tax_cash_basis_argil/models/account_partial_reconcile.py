# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from datetime import date

import logging
_logger = logging.getLogger(__name__)

class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"
    
    def _create_tax_cash_basis_moves(self):
        ''' Create the tax cash basis journal entries.
        :return: The newly created journal entries.
        '''
        tax_cash_basis_values_per_move = self._collect_tax_cash_basis_values()

        _logger.info("\n\ntax_cash_basis_values_per_move: %s\n" % tax_cash_basis_values_per_move)
        #ARGIL
        moves = self.env['account.move'].browse()
        aml_obj = self.env['account.move.line']
        moves_to_create = []
        to_reconcile_after = []
        for move_values in tax_cash_basis_values_per_move.values():
            move = move_values['move']
            pending_cash_basis_lines = []
            #ARGIL
            move_lines = []

            for partial_values in move_values['partials']:
                partial = partial_values['partial']

                # Init the journal entry.
                move_vals = {
                    'move_type': 'entry',
                    'date': partial.max_date,
                    'ref': move.name,
                    'journal_id': partial.company_id.tax_cash_basis_journal_id.id,
                    'line_ids': [],
                    'tax_cash_basis_rec_id': partial.id,
                    'tax_cash_basis_move_id': move.id,
                }

                # Tracking of lines grouped all together.
                # Used to reduce the number of generated lines and to avoid rounding issues.
                partial_lines_to_create = {}

                for line in move_values['to_process_lines']:
                    # to_process_lines = devuelve tuplas de lineas
                    line = line[1]
                    # ==========================================================================
                    # Compute the balance of the current line on the cash basis entry.
                    # This balance is a percentage representing the part of the journal entry
                    # that is actually paid by the current partial.
                    # ==========================================================================

                    # Percentage expressed in the foreign currency.
                    amount_currency = line.currency_id.round(line.amount_currency * partial_values['percentage'])
                    balance = partial_values['payment_rate'] and amount_currency / partial_values['payment_rate'] or 0.0

                    # ==========================================================================
                    # Prepare the mirror cash basis journal item of the current line.
                    # Group them all together as much as possible to reduce the number of
                    # generated journal items.
                    # Also track the computed balance in order to avoid rounding issues when
                    # the journal entry will be fully paid. At that case, we expect the exact
                    # amount of each line has been covered by the cash basis journal entries
                    # and well reported in the Tax Report.
                    # ==========================================================================

                    if line.tax_repartition_line_id:
                        # Tax line.

                        cb_line_vals = self._prepare_cash_basis_tax_line_vals(line, balance, amount_currency)
                        grouping_key = self._get_cash_basis_tax_line_grouping_key_from_vals(cb_line_vals)
                    elif line.tax_ids:
                        # Base line.

                        cb_line_vals = self._prepare_cash_basis_base_line_vals(line, balance, amount_currency)
                        grouping_key = self._get_cash_basis_base_line_grouping_key_from_vals(cb_line_vals)

                    if grouping_key in partial_lines_to_create:
                        aggregated_vals = partial_lines_to_create[grouping_key]['vals']

                        debit = aggregated_vals['debit'] + cb_line_vals['debit']
                        credit = aggregated_vals['credit'] + cb_line_vals['credit']
                        balance = debit - credit

                        aggregated_vals.update({
                            'debit': balance if balance > 0 else 0,
                            'credit': -balance if balance < 0 else 0,
                            'amount_currency': aggregated_vals['amount_currency'] + cb_line_vals['amount_currency'],
                        })

                        if line.tax_repartition_line_id:
                            aggregated_vals.update({
                                'tax_base_amount': aggregated_vals['tax_base_amount'] + cb_line_vals['tax_base_amount'],
                            })
                            partial_lines_to_create[grouping_key]['tax_line'] += line
                    else:
                        partial_lines_to_create[grouping_key] = {
                            'vals': cb_line_vals,
                        }
                        if line.tax_repartition_line_id:
                            partial_lines_to_create[grouping_key].update({
                                'tax_line': line,
                            })

                # ==========================================================================
                # Create the counterpart journal items.
                # ==========================================================================

                # To be able to retrieve the correct matching between the tax lines to reconcile
                # later, the lines will be created using a specific sequence.
                sequence = 0

                for grouping_key, aggregated_vals in partial_lines_to_create.items():
                    line_vals = aggregated_vals['vals']
                    line_vals['sequence'] = sequence

                    pending_cash_basis_lines.append((grouping_key, line_vals['amount_currency']))

                    if 'tax_repartition_line_id' in line_vals:
                        # Tax line.

                        tax_line = aggregated_vals['tax_line']
                        counterpart_line_vals = self._prepare_cash_basis_counterpart_tax_line_vals(tax_line, line_vals)
                        counterpart_line_vals['sequence'] = sequence + 1

                        if tax_line.account_id.reconcile:
                            move_index = len(moves_to_create)
                            to_reconcile_after.append((tax_line, move_index, counterpart_line_vals['sequence']))

                    else:
                        # Base line.

                        counterpart_line_vals = self._prepare_cash_basis_counterpart_base_line_vals(line_vals)
                        counterpart_line_vals['sequence'] = sequence + 1

                    sequence += 2

                    move_vals['line_ids'] += [(0, 0, counterpart_line_vals), (0, 0, line_vals)]
                    
                    #ARGIL
                    partial = move_values['partials'][0]['partial'] # Registro de conciliacion
                    # -- Tomamos la poliza del pago para agregarle las partidas.
                    xmove_id = partial.debit_move_id.move_id.id if partial.debit_move_id.move_id.id != move.id else partial.credit_move_id.move_id.id
                    counterpart_line_vals['move_id'] = xmove_id
                    line_vals['move_id'] = xmove_id
                    move_lines.append(counterpart_line_vals)
                    move_lines.append(line_vals)                    
                    
                _logger.info("\nmove_lines: %s" % move_lines)
                #raise ValidationError("Pausa")
                amls = aml_obj.with_context({'check_move_validity':False}).create(move_lines)
                moves += move
                moves_to_create.append(move_vals)
                
        #moves = self.env['account.move'].create(moves_to_create)
        #moves._post(soft=False)

        # Reconcile the tax lines being on a reconcile tax basis transfer account.
        for line, move_index, sequence in to_reconcile_after:
            counterpart_line = moves[move_index].line_ids.filtered(lambda line: line.sequence == sequence)

            # When dealing with tiny amounts, the line could have a zero amount and then, be already reconciled.
            if counterpart_line.reconciled:
                continue

            (line + counterpart_line).reconcile()

        return moves