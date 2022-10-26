# -*- encoding: utf-8 -*-   
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from suds.client import Client, WebFault
from suds.plugin import MessagePlugin
from xml.dom.minidom import parse, parseString
from . import cancelation_codes ## Clase con Mucha Informacion
import logging
_logger = logging.getLogger(__name__)

class LogPlugin(MessagePlugin):
    def sending(self, context):
        _logger.info(str(context.envelope))
        #print(str(context.envelope))
        return
    def received(self, context):
        _logger.info(str(context.reply))
        #print(str(context.reply))
        return

    
class AccountMove(models.Model):
    _inherit = 'account.move'
    
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
    
    
    uuid_relacionado_cancelacion = fields.Char(string="UUID Relacionado en Cancelación", copy=False)
    



    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    