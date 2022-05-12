# -*- encoding: utf-8 -*-
# Coded by German Ponce Dominguez 
#     ▬▬▬▬▬.◙.▬▬▬▬▬  
#       ▂▄▄▓▄▄▂  
#    ◢◤█▀▀████▄▄▄▄▄▄ ◢◤  
#    █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬  
#    ◥ █████ ◤  
#     ══╩══╩═  
#       ╬═╬  
#       ╬═╬ Dream big and start with something small!!!  
#       ╬═╬  
#       ╬═╬ You can do it!  
#       ╬═╬   Let's go...
#    ☻/ ╬═╬   
#   /▌  ╬═╬   
#   / \
# Cherman Seingalt - german.ponce@outlook.com

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from datetime import date

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit ='account.move'

    invoice_reversed = fields.Boolean('Factura con Nota de Credito')
    # refund_id = fields.Many2one('account.move', 'Nota de Credito')
    invoice_origin_reverse_id = fields.Many2one('account.move', 'Factura Origen')

class AccountMoveLine(models.Model):
    _inherit ='account.move.line'

    def _create_exchange_difference_move(self):
        contain_invoice = False
        contain_refund = False
        for line in self:
            if line.move_id.move_type in ('out_invoice', 'in_invoice'):
                contain_invoice = True
            elif line.move_id.move_type in ('out_refund', 'in_refund'):
                contain_refund = True
        if contain_invoice and contain_refund:
            _logger.info("\n######### Es una conciliación de factura contra nota de credito >>>>>>>>>>>> ")
            _logger.info("\n######### No creamos partida de diferencia de cambio >>>>>>>>>>>> ")
            return False
        res = super(AccountMoveLine, self)._create_exchange_difference_move()
        return res


    def reconcile(self):
        ''' Reconcile the current move lines all together.
        :return: A dictionary representing a summary of what has been done during the reconciliation:
                * partials:             A recorset of all account.partial.reconcile created during the reconciliation.
                * full_reconcile:       An account.full.reconcile record created when there is nothing left to reconcile
                                        in the involved lines.
                * tax_cash_basis_moves: An account.move recordset representing the tax cash basis journal entries.
        '''
        results = {}

        if not self:
            return results

        # List unpaid invoices
        not_paid_invoices = self.move_id.filtered(
            lambda move: move.is_invoice(include_receipts=True) and move.payment_state not in ('paid', 'in_payment')
        )

        # ==== Check the lines can be reconciled together ====
        company = None
        account = None
        for line in self:
            # if line.reconciled:
            #     raise UserError(_("You are trying to reconcile some entries that are already reconciled."))
            if not line.account_id.reconcile and line.account_id.internal_type != 'liquidity':
                raise UserError(_("Account %s does not allow reconciliation. First change the configuration of this account to allow it.")
                                % line.account_id.display_name)
            if line.move_id.state != 'posted':
                raise UserError(_('You can only reconcile posted entries.'))
            if company is None:
                company = line.company_id
            elif line.company_id != company:
                raise UserError(_("Entries doesn't belong to the same company: %s != %s")
                                % (company.display_name, line.company_id.display_name))
            if account is None:
                account = line.account_id
            elif line.account_id != account:
                raise UserError(_("Entries are not from the same account: %s != %s")
                                % (account.display_name, line.account_id.display_name))

        sorted_lines = self.sorted(key=lambda line: (line.date_maturity or line.date, line.currency_id))

        # ==== Collect all involved lines through the existing reconciliation ====

        involved_lines = sorted_lines
        involved_partials = self.env['account.partial.reconcile']
        current_lines = involved_lines
        current_partials = involved_partials
        while current_lines:
            current_partials = (current_lines.matched_debit_ids + current_lines.matched_credit_ids) - current_partials
            involved_partials += current_partials
            current_lines = (current_partials.debit_move_id + current_partials.credit_move_id) - current_lines
            involved_lines += current_lines

        # ==== Create partials ====

        partials = self.env['account.partial.reconcile'].create(sorted_lines._prepare_reconciliation_partials())

        # Track newly created partials.
        results['partials'] = partials
        involved_partials += partials

        # ==== Create entries for cash basis taxes ====

        is_cash_basis_needed = account.user_type_id.type in ('receivable', 'payable')
        if is_cash_basis_needed and not self._context.get('move_reverse_cancel'):
            tax_cash_basis_moves = partials._create_tax_cash_basis_moves()
            results['tax_cash_basis_moves'] = tax_cash_basis_moves

        # ==== Check if a full reconcile is needed ====

        if involved_lines[0].currency_id and all(line.currency_id == involved_lines[0].currency_id for line in involved_lines):
            is_full_needed = all(line.currency_id.is_zero(line.amount_residual_currency) for line in involved_lines)
        else:
            is_full_needed = all(line.company_currency_id.is_zero(line.amount_residual) for line in involved_lines)

        if is_full_needed:

            # ==== Create the exchange difference move ====

            if self._context.get('no_exchange_difference'):
                exchange_move = None
            else:
                exchange_move = involved_lines._create_exchange_difference_move()
                if exchange_move:
                    exchange_move_lines = exchange_move.line_ids.filtered(lambda line: line.account_id == account)

                    # Track newly created lines.
                    involved_lines += exchange_move_lines

                    # Track newly created partials.
                    exchange_diff_partials = exchange_move_lines.matched_debit_ids \
                                             + exchange_move_lines.matched_credit_ids
                    involved_partials += exchange_diff_partials
                    results['partials'] += exchange_diff_partials

                    exchange_move._post(soft=False)

            # ==== Create the full reconcile ====

            results['full_reconcile'] = self.env['account.full.reconcile'].create({
                'exchange_move_id': exchange_move and exchange_move.id,
                'partial_reconcile_ids': [(6, 0, involved_partials.ids)],
                'reconciled_line_ids': [(6, 0, involved_lines.ids)],
            })

        # Trigger action for paid invoices
        not_paid_invoices\
            .filtered(lambda move: move.payment_state in ('paid', 'in_payment'))\
            .action_invoice_paid()

        return results


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def _prepare_default_reversal(self, move):
        res = super(AccountMoveReversal, self)._prepare_default_reversal(move=move)
        move.invoice_reversed = True
        res.update({
                        'invoice_origin_reverse_id': move.id,
                    })
        return res

class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def _create_tax_cash_basis_moves(self):
        for partial in self:
            debit_move_type = partial.debit_move_id.move_id.move_type
            credit_move_type = partial.credit_move_id.move_id.move_type
            if debit_move_type == 'out_invoice' and credit_move_type == 'out_refund':
                _logger.info("\n######### Es una conciliación de factura contra nota de credito >>>>>>>>>>>> ")
                _logger.info("\n######### No creamos partida de reclasificación de Impuestos >>>>>>>>>>>> ")
                return False
            elif credit_move_type == 'out_invoice' and debit_move_type == 'out_refund':
                _logger.info("\n######### Es una conciliación de factura contra nota de credito >>>>>>>>>>>> ")
                _logger.info("\n######### No creamos partida de reclasificación de Impuestos >>>>>>>>>>>> ")
                return False
            elif debit_move_type == 'in_invoice' and credit_move_type == 'in_refund':
                _logger.info("\n######### Es una conciliación de factura contra nota de credito >>>>>>>>>>>> ")
                _logger.info("\n######### No creamos partida de reclasificación de Impuestos >>>>>>>>>>>> ")
                return False
            elif credit_move_type == 'in_invoice' and debit_move_type == 'in_refund':
                _logger.info("\n######### Es una conciliación de factura contra nota de credito >>>>>>>>>>>> ")
                _logger.info("\n######### No creamos partida de reclasificación de Impuestos >>>>>>>>>>>> ")
                return False
        res = super(AccountPartialReconcile, self)._create_tax_cash_basis_moves()
        return res
