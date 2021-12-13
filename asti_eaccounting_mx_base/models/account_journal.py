# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree as et

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    #journal_type    = fields.Many2one('account.journal.types', 'Tipo de Póliza')
    cmpl_type       = fields.Selection([('check', 'Cheque'), 
                                        ('transfer', 'Transferencia'), 
                                        ('payment', 'Otro método de pago')], 
                                       string='Tipo de complemento', 
                                       help='Indique el tipo de complemento que este diario generará en las pólizas.')
    #credit_cmpl_acc_id = fields.Many2one('eaccount.bank.account', string='Cuenta bancaria acreedora', 
    #                                     help='Especifique la cuenta bancaria a utilizar en los complementos de contabilidad electrónica')
    #debit_cmpl_acc_id = fields.Many2one('eaccount.bank.account', string='Cuenta bancaria deudora', 
    #                                    help='Especifique la cuenta bancaria a utilizar en los complementos de contabilidad electrónica')
    other_payment   = fields.Many2one('eaccount.payment.methods', string='Método de Pago SAT')


