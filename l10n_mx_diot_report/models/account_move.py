# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AccountInvoiceLineVATImport(models.Model):
    _name ='account.invoice.line.vatimport'
    _description ="Lineas de IVA de Importaciones asociadas a factura"

    invoice_line_id = fields.Many2one('account.move.line', string="Línea de Factura", required=True, ondelete='cascade')
    invoice_id  = fields.Many2one('account.move', related='invoice_line_id.move_id', string="Factura", store=True)
    partner_id  = fields.Many2one('res.partner', string="Proveedor Extranjero", required=True)
    date        = fields.Date(string='Fecha Efectiva', required=True, help="Fecha efectiva para tomar para la DIOT")
    amount_base = fields.Float(string="Base IVA Acreditable", digits='Product Price', required=True, default=0.0)
    tax_amount  = fields.Float(string="Monto IVA Importaciones", digits='Product Price', required=True, default=0.0)
    line_type   = fields.Selection([('iva_16_acred', 'IVA 16% Acreditable'),
                                    ('iva_16_no_acred', 'IVA 16% NO Acreditable'),
                                    ('iva_exento', 'IVA Exento'),
                                   ], string="Tipo", required=True)
    #no_acreditable = fields.Boolean(string='No acreditable', default=False, help="Marque esta casilla si el IVA de Importaciones NO ES ACREDITABLE.")
    invoice_state = fields.Selection(related='invoice_id.state', string="Estado Factura", store=True)
    account_id  = fields.Many2one('account.account', string="Cuenta Contable",
                                  check_company=True, required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Cuenta Analítica', check_company=True,
                                          domain=[('account_type', '=', 'normal')])
    analytic_tag_ids = fields.Many2many('account.analytic.tag', 
                                        'vatimport_analitic_line_rel', 'analytic_id', 'line_id', 
                                        string='Etiquetas Analíticas', check_company=True)
    name = fields.Text(string="Descripción", required=True)
    
class AccountMoveLine(models.Model):
    _inherit ='account.move.line'
    
    vat_line_ids = fields.One2many('account.invoice.line.vatimport', 'invoice_line_id', string="Integración IVA Importaciones")

    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        result = super(AccountMoveLine, self)._onchange_product_id()
        if self.product_id and self.product_id.import_vat:
            warning = {
                    'title': _('Advertencia!'),
                    'message': _('No puede agregar el IVA de Importaciones directamente. Por favor realice esto con el Asistente !'),
                }
            return {'warning': warning}            
        return result  
    
class AccountMove(models.Model):
    _inherit ='account.move'
    
    @api.depends('vat_line_ids')
    def _check_if_vat_line_ids(self):
        for rec in self:
            rec.has_vat_lines = bool(rec.move_type == 'in_invoice' and rec.vat_line_ids) 
    
    vat_line_ids  = fields.One2many('account.invoice.line.vatimport', 'invoice_id', string="Integración IVA Importaciones")    
    has_vat_lines = fields.Boolean(compute="_check_if_vat_line_ids",string="Tiene líneas de IVA Importaciones")
    
    
    
class AccountInvoiceVATImportWizardLine(models.TransientModel):
    _name = 'account.invoice.line.vatimport.wizard.line'
    _description = 'Wizard Lineas de Factura para IVa Importaciones1'

    wizard_id   = fields.Many2one('account.invoice.line.vatimport.wizard', string="Wizard", required=False, ondelete='cascade')
    partner_id  = fields.Many2one('res.partner', string="Proveedor Extranjero", required=True)
    date        = fields.Date(string='Fecha Efectiva', required=True, help="Fecha efectiva para tomar para la DIOT")
    amount_base = fields.Float(string="Monto Base", digits='Product Price', required=True, default=0.0)
    tax_amount  = fields.Float(string="Monto IVA", digits='Product Price', required=True, default=0.0)
    line_type   = fields.Selection([('iva_16_acred', 'IVA 16% Acreditable'),
                                    ('iva_16_no_acred', 'IVA 16% NO Acreditable'),
                                    ('iva_exento', 'IVA Exento'),
                                   ], string="Tipo", required=True)
    
    #company_id = fields.Many2one('res.company', string='Compañía',
    #                             default=lambda self: self.env.company.id)
    account_id  = fields.Many2one('account.account', string="Cuenta Contable",
                                  required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta Analítica',
                                          domain=[('account_type', '=', 'normal')])
    analytic_tag_ids = fields.Many2many('account.analytic.tag', 
                                        'wiz_vatimport_analitic_line_rel', 'analytic_id', 'line_id', 
                                        string='Etiquetas Analíticas')
    name = fields.Text(string="Descripción", required=True)

    @api.onchange('account_id')
    def _onchange_account_id(self):
        self.name=self.account_id.name
    
    
class AccountInvoiceVATImportWizard(models.TransientModel):
    _name = 'account.invoice.line.vatimport.wizard'
    _description = 'Wizard Lineas de Factura para IVa Importaciones2'    
    
    #product_name = fields.Char(string="Descripción", required=True)
    #account_analytic_id = fields.Many2one('account.analytic.account', string='Cuenta Analítica', domain=[('account_type', '=', 'normal')])
    line_ids = fields.One2many('account.invoice.line.vatimport.wizard.line', 'wizard_id',
                                string="Detalle IVA Importaciones", required=True)
    company_id = fields.Many2one('res.company', string='Compañía', required=True,
                                 default=lambda self: self.env.company.id)

    def button_add_invoice_line(self):
        if not self.line_ids:
            raise UserError(_("Advertencia ! No ha agregado ninguna línea, favor de revisar."))
        active_model = self._context.get('active_model')
        active_ids = self._context.get('active_ids')
        active_id = self._context.get('active_id')
        # Checks on context parameters
        if not active_model or not active_ids:
            raise UserError(_("Error de programación: La acción disparada por el asistente no puede ser procesada sin 'active_model' y/o sin 'active_ids' en el contexto."))
        if active_model != 'account.move':
            raise UserError(_("Error de Programación: El modelo esperado para esta acción es 'account.move'. El modelo actual es '%s'.") % active_model)
        
        product = self.env['product.product'].search([('import_vat','=',1)], limit=1)
        if not product:
            raise UserError(_("Error ! No tiene definido un Producto como IVA de Importaciones"))        
        invoice = self.env['account.move'].browse(active_ids)
        if invoice.state != 'draft':
            raise UserError(_("Error ! No puede agregar Impuestos de Importación si la factura no se encuentra en Estado Borrador "))
        if invoice.move_type != 'in_invoice':
            raise UserError(_("Error ! No puede agregar Impuestos de Importación en Facturas que no sean de Proveedor"))
            
        aml_obj = self.env['account.move.line']
        vat_lines = []
        suma = 0.0
        for line in self.line_ids:
            xline = (0,0, {
                'name'       : line.name,
                'partner_id' : line.partner_id.id,
                'date'       : line.date,
                'amount_base': line.amount_base,
                'tax_amount' : line.tax_amount,
                'line_type'  : line.line_type,
                'account_id' : line.account_id.id,
                'analytic_account_id' : line.analytic_account_id.id,
                'analytic_tag_ids' : [(6,0, line.analytic_tag_ids.ids)],
            })
            suma += line.tax_amount
        
            invoice_line = {
                'name'          : line.name,
                'move_id'       : invoice.id,
                'account_id'    : line.account_id.id,
                'analytic_account_id' : line.analytic_account_id.id,
                'analytic_tag_ids' : [(6,0, line.analytic_tag_ids.ids)],
                'quantity'      : 1.0,
                'price_unit'    : line.tax_amount,
                'product_id'    : product.id,
                'product_uom_id': product.uom_id.id,
                'tax_ids'       : [],
                'vat_line_ids'  : [xline],
            }
            res = aml_obj.with_context(check_move_validity=False).create(invoice_line)
        if suma:
            move_line = invoice.line_ids.filtered(lambda x: x.account_id.internal_type=='payable')
            move_line.credit = move_line.credit + suma
        return True
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
