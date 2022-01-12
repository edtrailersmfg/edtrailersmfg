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

from odoo import api, fields, models
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