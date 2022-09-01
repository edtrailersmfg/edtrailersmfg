# -*- coding: utf-8 -*-
from odoo import api, models, fields, tools, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountCFDICancelSAT(models.TransientModel):
    _name = 'account.cfdi.cancel.sat'
    _description = 'Wizard para solicitar la Cancelacion del CFDI de acuerdo a nuevo esquema de cancelacion del SAT'
    
    invoice_id = fields.Many2one('account.move', required=False, string="Factura a Cancelar")
    payment_id = fields.Many2one('account.payment', required=False, string="Pago a Cancelar")
    
    motivo_cancelacion = fields.Selection([
        ('01', '[01] Comprobantes emitidos con errores con relación'),
        ('02', '[02] Comprobantes emitidos con errores sin relación'),
        ('03', '[03] No se llevó a cabo la operación'),
        ('04', '[04] Operación nominativa relacionada en una factura global')
    ], required=True, default='03', string="Motivo Cancelación")
    
    
    uuid_relacionado_cancelacion = fields.Char(string="UUID Relacionado en Cancelación")
    
    
    @api.model
    def default_get(self, default_fields):
        res = super(AccountCFDICancelSAT, self).default_get(default_fields)
        if self._context.get('active_model') == 'account.move':
            invoice = self.env['account.move'].browse(self._context.get('active_ids', []))
            payment = False
            if invoice.motivo_cancelacion: 
                raise ValidationError(_('Advertencia ! Ya se había solicitado la Cancelación de este CFDI, por favor revise'))
        elif self._context.get('active_model') == 'account.payment':
            payment = self.env['account.payment'].browse(self._context.get('active_ids', []))
            invoice = False
            if payment.motivo_cancelacion: 
                raise ValidationError(_('Advertencia ! Ya se había solicitado la Cancelación de este CFDI, por favor revise'))
                
        
        res.update({
            'invoice_id' : invoice and invoice.id or False,
            'payment_id' : payment and payment.id or False
        })
        
        return res
        
        
    def request_cancel(self):
        if self.invoice_id:
            self.invoice_id.write({'motivo_cancelacion' : self.motivo_cancelacion,
                                   'uuid_relacionado_cancelacion' : self.uuid_relacionado_cancelacion,
                                  })
            self.invoice_id.button_cancel_posted_moves()
        if self.payment_id:
            self.payment_id.write({'motivo_cancelacion' : self.motivo_cancelacion,
                                   'uuid_relacionado_cancelacion' : self.uuid_relacionado_cancelacion,
                                  })
            self.payment_id.move_id.write({'motivo_cancelacion' : self.motivo_cancelacion,
                                           'uuid_relacionado_cancelacion' : self.uuid_relacionado_cancelacion,

                                          })
            self.payment_id.action_cancel()
        return True