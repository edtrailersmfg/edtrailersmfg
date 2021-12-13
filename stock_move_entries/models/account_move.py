# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
        
class account_move(models.Model):
    _inherit = "account.move"

    
    def show_stock_moves(self):
        self.ensure_one()
        if not self.stock_move_id:
            return False
        
        return {
                'domain': "[('id','in',[" + str(self.stock_move_id.id) + "])]",
                'name'      : _('Movimientos de Inventario'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'context': {'tree_view_ref': 'stock.view_move_tree'},
                'res_model': 'stock.move',
                'type': 'ir.actions.act_window',
            }        



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: