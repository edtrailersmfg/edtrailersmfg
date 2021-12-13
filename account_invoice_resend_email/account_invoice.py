# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
import logging
_logger = logging.getLogger(__name__)


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'
    
    
    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        res = super(MailComposer, self)._onchange_template_id(template_id, composition_mode, model, res_id)
        if model not in ('account.move','account.payment') or not self._context.get('resend', False):
            return res
        attachment_obj = self.env['ir.attachment']
        rec = self.env[model].browse([res_id])
        
        attachment_ids = attachment_obj.search([('res_model', '=', model), 
                                                ('res_id', '=', res_id), 
                                                ('name','ilike', '.xml'),
                                                ], limit=1)
        _logger.info("res: %s" % res)
        _logger.info("res.keys(): %s" % res.keys())
        
        if attachment_ids:
            res['value']['attachment_ids'][0][2].append(attachment_ids.id)
        return res
        

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    def action_invoice_sent(self):
        res = super(AccountInvoice, self).action_invoice_sent()
        context = res['context']
        context.update({'resend': 1})
        res.update({'context':context})
        return res

