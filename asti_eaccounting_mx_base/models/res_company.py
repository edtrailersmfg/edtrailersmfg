# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from hashlib import sha256 # Contabilidad 1.3
from lxml import etree as et
import logging

class account_move_concept_template(models.Model):
    _name = 'account.move.concept.template'
    _description = "Template para concepto de pólizas (Contab. Electr.)"

    move_type = fields.Selection([
                        ('in_invoice', 'Factura de Proveedor'),
                        ('out_invoice', 'Factura de Cliente'),
                        ('out_refund', 'Nota de Crédito de Cliente'),
                        ('outbound', 'Pago a Proveedor'),
                        ('inbound', 'Cobro de Cliente'),
                        ('in_refund', 'Nota de Crédito de Proveedor')], 
                    required=True, string='Tipo de póliza', 
        help='Elija el tipo de póliza para la cual aplicar esta plantilla. Solo puede haber una plantilla por tipo.')
    concept = fields.Text(string='Concepto', help='Escriba la plantilla, considere que el límite máximo son 300 caracteres una vez aplicado el formato.', required=True)
    company_id = fields.Many2one('res.company', string='Compañía', required=True)
                
    _sql_constraints = [('unique_move_type', 'unique(move_type, company_id)', 'Solamente puede haber una plantilla por tipo de póliza en cada empresa.')]


class ResCompany(models.Model):
    _inherit = 'res.company'
    

    #regname = fields.Char(string='Razón social', size=250, required=True)
    #rfc = fields.Char(string='R.F.C.', size=15, required=True, help="RFC de la empresa SIN el prefijo MX")
    #mobile_number = fields.Char(string='Móvil', size=50)
    #block = fields.Char(string='Colonia', size=200)
    accounts_config_done = fields.Boolean(string='Accounts config done')
    license_key = fields.Char(string='Clave de licenciamiento', size=40)
    """
    apply_in_check = fields.Boolean(string='Cheque')
    apply_in_trans = fields.Boolean(string='Transferencia')
    apply_in_cfdi = fields.Boolean(string='Comprobante CFDI')
    apply_in_other = fields.Boolean(string='Comp. Otro')
    apply_in_forgn = fields.Boolean(string='Comp. Extranjero')
    apply_in_paymth = fields.Boolean(string='Método de Pago')
    """
    concept_template_ids = fields.One2many('account.move.concept.template', 'company_id', 'Plantillas de Conceptos')
    auto_mode_enabled = fields.Boolean(string='Modo automático (C.E.)', default=True,
                                       help='Marque esta casilla para proporcionar las características de automatización en la contabilidad electrónica; se requiere una nueva clave de licenciamiento para activación.')
    
    def _assembly_concept(self, mv_type, invoice=None, voucher=None):
        self.ensure_one()
        if mv_type == 'in_invoice':
            move = 'Facturas de Proveedor'
        elif mv_type == 'out_invoice':
            move = 'Facturas de Cliente'
        elif mv_type == 'out_refund':
            move = u'Notas de Cr\xe9dito de cliente'
        elif mv_type == 'outbound':
            move = 'Pagos a Proveedor'
        elif mv_type == 'inbound':
            move = 'Cobros de Cliente'
        elif mv_type == 'out_refund':
            move = u'Notas de Cr\xe9dito de Proveedor'
        templates = [ ln.concept for ln in self.concept_template_ids if ln.move_type == mv_type ]
        if len(templates):
            concept_parts = templates[0].split('___')
            if len(concept_parts) != 2:
                raise UserError(_('Plantilla de concepto incorrecta.\n\nRevise que la plantilla para %s cuenta con argumentos.') % (move))
            try:
                return concept_parts[0] % eval(concept_parts[1])
            except Exception as e:
                logging.getLogger(self._name).exception('Error evaluating Template for Account Move Concept.')
                logging.getLogger(self._name).exception(e)
                raise UserError(_('Plantilla de concepto errónea\n\nRevise que la plantilla para %s cuenta con el formato requerido y que los campos especificados existen en el modelo.') % (move))
        return False

