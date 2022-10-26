# -*- encoding: utf-8 -*-   
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    #####################################
    #cfdi_pac                = fields.Selection(selection_add=[('pac_sifei', 'SIFEI - https://www.sifei.com.mx')], #string='CFDI Pac', readonly=True, store=True, copy=False, default='pac_sifei',
    #                                           ondelete={'pac_sifei': 'set null'})
    #####################################        
    motivo_cancelacion = fields.Selection([
        ('01', '[01] Comprobantes emitidos con errores con relación'),
        ('02', '[02] Comprobantes emitidos con errores sin relación'),
        ('03', '[03] No se llevó a cabo la operación'),
        ('04', '[04] Operación nominativa relacionada en una factura global')
    ], required=False, string="Motivo Cancelación", copy=False)
    
    
    uuid_relacionado_cancelacion = fields.Char(string="UUID Relacionado en Cancelación")
    
    
    def action_draft(self):
        if self.payment_type == 'inbound' and self.l10n_mx_edi_cfdi_uuid and not self.motivo_cancelacion:
            return {
            'name': _('Solicitar Cancelación'),
            'res_model': 'account.cfdi.cancel.sat',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.payment',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
        return super(AccountPayment, self).action_draft()
            
            