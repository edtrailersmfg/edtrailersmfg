# -*- encoding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'
        
    @api.multi
    def print_account_move(self):
        #print "Entrando a intentar imprimir el reporte"
        try:
            return self.env['report'].get_action(self, 'account_move_report.report_accountmove')    
        except:
            #print "Error al mandar a llamar el reporte, revisar..."
            return False
