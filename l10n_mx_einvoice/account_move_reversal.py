# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'
    
    def _prepare_default_reversal(self, move):
        res = super(AccountMoveReversal, self)._prepare_default_reversal(move)
        if move.move_type == 'out_invoice':
            uso_cfdi_id = self.env['sat.uso.cfdi'].search([('code','=','G02')], limit=1)
            metodo_pago_id = self.env['sat.metodo.pago'].search([('code','=','PUE')], limit=1)
            pay_method_id = self.env['pay.method'].search([('code','=','99')], limit=1)
            type_rel_id = self.env['sat.tipo.relacion.cfdi'].search([('code','=','01')], limit=1)
            res.update({'uso_cfdi_id'    : uso_cfdi_id.id,
                        'metodo_pago_id' : metodo_pago_id.id,
                        'pay_method_id'  : pay_method_id.id,
                        'pay_method_ids' : [(6,0,[pay_method_id.id])],
                        'type_rel_id'    : type_rel_id.id,
                        'type_rel_cfdi_ids' : [(0,0,{'invoice_id'     : move.id,
                                                     'invoice_rel_id' : move.id})],
                       })
        return res