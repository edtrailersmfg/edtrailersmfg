# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    
    def show_entry_lines(self):
        res = []
        for picking in self:
            for move in picking.move_lines:
                res += move.account_move_ids.ids
        aml_ids = self.env['account.move.line'].search([('move_id','in',res)])
        action_ref = self.env.ref('account.action_account_moves_all_a')
        if not action_ref:
            return False
        action_data = action_ref.read()[0]
        action_data['domain'] = [('id', 'in', aml_ids.ids)]
        return action_data
                


    
    def show_journal_entries(self):
        res = []
        for picking in self:
            for move in picking.move_lines:
                res += move.account_move_ids.ids
                
        action_ref = self.env.ref('account.action_move_journal_line')
        if not action_ref:
            return False
        action_data = action_ref.read()[0]
        action_data['domain'] = [('id', 'in', res)]
        return action_data
        

class stock_move(models.Model):
    _inherit = "stock.move"
    
    
    @api.depends('state', 'product_uom_qty','price_unit')
    def _calc_amount_stock_move(self):
        context = dict(self._context or {})        
        for move in self:
            move.amount_stock_move = move.product_qty * (move.price_unit or 0.0)

    amount_stock_move     = fields.Float(compute='_calc_amount_stock_move', string='Monto Movimiento', 
                                         digits='Product Price', store=True, readonly=True)
"""
class stock_quant(osv.osv):
    _inherit = "stock.quant"
    
    if release.major_version == "9.0":    
        def _prepare_account_move_line(self, cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=None):
            res = super(stock_quant, self)._prepare_account_move_line(cr, uid, move, qty, cost, credit_account_id, debit_account_id, context)
            if res: # Para el caso de una Recepcion de Proveedor con cantidad mayor a la solicitada y sin precio promedio previo.
                res[0][2]['stock_move_id'] = move.id
                res[1][2]['stock_move_id'] = move.id
            return res
"""
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: