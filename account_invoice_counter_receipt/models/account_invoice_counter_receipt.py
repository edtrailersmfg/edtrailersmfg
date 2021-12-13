# -*- coding: utf-8 -*-
#
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from datetime import date, datetime, timedelta



class AccountInvoiceCounterReceipt(models.Model):
    _name = "account.invoice.counter.receipt"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Contra Recibos de Facturas"
    _order = "name desc"
    
    
    
    @api.depends('state', 'partner_id', 'payment_term_id', 'date')
    def _get_date_due(self):
        for record in self:
            if not record.partner_id or not record.date or not record.payment_term_id:
                record.date_due=False
            else:
                date_due = False
                _logger.info("record.payment_term_id: %s" % record.payment_term_id)
                pterm_list = record.payment_term_id.compute(value=1, date_ref=record.date)
                if not pterm_list:
                    record.date_due = record.date
                else:
                    pterm_list = [line[0] for line in pterm_list]
                    pterm_list.sort()
                    date_due = pterm_list[-1]
                    record.date_due = date_due

    
    
    @api.depends('state', 'invoice_m2m_ids')
    def _get_computed_data(self):
        for rec in self:
            if not rec.invoice_m2m_ids:
                return
            rec.currency_id = rec.invoice_m2m_ids[0].currency_id
            rec.amount_total = sum(rec.invoice_m2m_ids.mapped('amount_total'))
            rec.amount_residual = sum(rec.invoice_m2m_ids.mapped('amount_residual'))
            rec.amount_total_text = self._get_amount_to_text(self.amount_total, self.currency_id)
            rec.amount_residual_text = self._get_amount_to_text(self.amount_residual, self.currency_id)
            
    
    name    = fields.Char("Contra-recibo", required=True, default="/", 
                          readonly=True, index=True)
    move_type    = fields.Selection([('out_invoice', 'Facturas de Cliente'),
                                ('in_invoice', 'Facturas de Proveedor'),
                               ], required=True, index=True)
    state   = fields.Selection([('draft', 'Borrador'),
                                ('confirmed', 'Confirmado'),
                                ('cancel', 'Cancelado'),
                               ], required=True, default='draft', readonly=True,
                               index=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Empresa", readonly=True, required=True, tracking=True,
                                 states={'draft':[('readonly',False)]}, index=True)
    
    date    = fields.Date("Fecha", required=True, readonly=True, tracking=True,
                          default=lambda self: fields.Date.context_today(self),
                          states={'draft':[('readonly',False)]})
    date_due = fields.Date("Vencimiento", compute="_get_date_due")
    
    payment_term_id = fields.Many2one('account.payment.term', 'Plazo de Pago', required=True,readonly=True, 
                                 states={'draft':[('readonly',False)]}, index=True)
    
    amount_total    = fields.Monetary(string="Total Facturas", compute="_get_computed_data", store=True)
    amount_residual = fields.Monetary(string="Saldo Facturas", compute="_get_computed_data", store=True)
    amount_total_text = fields.Char('Total en Texto', compute="_get_computed_data", store=True)
    amount_residual_text = fields.Char('Saldo en Texto', compute="_get_computed_data", store=True)
    currency_id     = fields.Many2one('res.currency', string="Moneda",
                                      compute="_get_computed_data", store=True)
    
    invoice_ids = fields.One2many('account.move', 'counter_receipt_id', readonly=True, tracking=True,
                                  domain="[('move_type','in',('out_invoice','out_refund','in_invoice','in_refund'))]",
                                 string="Facturas y Notas de Crédito")
    
    invoice_m2m_ids = fields.Many2many('account.move', 'account_invoice_counter_receipt_rel', 
                                       'counter_receipt_id', 'invoice_id',
                                      string="Facturas y Notas de Crédito a seleccionar",
                                      readonly=True, states={'draft':[('readonly',False)]})

    notes   = fields.Text("Observaciones", readonly=True, tracking=True,
                          states={'draft':[('readonly',False)]})
    
    company_id = fields.Many2one('res.company', string='Company', tracking=True,
                                 default=lambda self: self.env.user.company_id, 
                                 states={'draft':[('readonly',False)]})
    
    
    @api.constrains('parent_id')
    def _check_validations(self):
        """ Validamos que todas las facturas tengan la misma moneda y 
            que el estado de las Facturas sea "Abierto"
        """
        for rec in self:
            if any(inv.state!='posted' and inv.payment_state!='not_paid' for inv in rec.invoice_ids):
                raise ValidationError(_("Error de captura !!!\n\nUna de las facturas seleccionadas NO se encuentra Abierta"))
            if any(inv.currency_id!= rec.invoice_ids[0].currency_id for inv in rec.invoice_ids):
                raise ValidationError(_("Error de captura !!!\n\nNo puede incluir facturas de diferente moneda"))
        return True

    """
    @api.onchange('type')
    def _onchange_type(self):
        if not self.type:
            return {'domain': {'partner_id': []}}
        elif self.type=='customer':
            return {'domain': {'partner_id': [('customer','=',1)]}}
        else:
            return {'domain': {'partner_id': [('supplier','=',1)]}}
    """
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.move_type == 'in_invoice':
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id
        else:
            self.partner_id.property_payment_term_id.id
    
    @api.model
    def create(self, vals):
        if vals['move_type'] == 'out_invoice':
            vals['name'] = self.env['ir.sequence'].next_by_code('account.invoice.counter.receipt.customer') or '/'
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code('account.invoice.counter.receipt.supplier') or '/'
        if vals['name']=='/':
            raise ValidationError(_("Error! Secuencia incorrecta"))
        if not vals.get('invoice_m2m_ids', False) or not vals['invoice_m2m_ids'][0] or not vals['invoice_m2m_ids'][0][2]:
            raise ValidationError(_("Validación\n\nNo puede guardar un registro sin haber seleccionado por lo menos una factura."))
        res = super(AccountInvoiceCounterReceipt, self).create(vals)
        invoices = self.env['account.move'].browse(vals['invoice_m2m_ids'][0][2])
        for inv in invoices:
            if inv.counter_receipt_id and inv.counter_receipt_id.id != res.id and \
               inv.counter_receipt_id.state in ('draft','confirmed'):
                raise ValidationError(_("Validación\n\nLa factura %s - %s ya se encuentra relacionada a otro documento.") % (inv.number, inv.reference))
        invoices.write({'counter_receipt_id' : res.id})
        res.action_confirm()
        return res

    
    def _get_amount_to_text(self, amount, currency_id):
        currency = currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(amount, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(amount_d * 100)
        words = self.company_id.currency_id.with_context(lang=self.env.user.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
        return '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(words=words, amount_d=amount_d, curr_t=currency_type)
    
    
    
    def action_confirm(self):
        for record in self.filtered(lambda x: x.state == 'draft'):
            for invoice in record.invoice_ids:
                if invoice.invoice_date_due == record.date_due:
                    continue
                days = (record.date_due - invoice.invoice_date_due).days
                if days != 0:
                    res = invoice.write({'invoice_date_due': record.date_due, 
                                          'original_date_due': invoice.invoice_date_due})
                    for ml in invoice.line_ids.filtered(lambda x: x.account_id.internal_type in ('receivable', 'payable')):
                        xres = ml.date_maturity + timedelta(days=days)
                        ml.write({'date_maturity': xres, 'original_date_maturity': ml.date_maturity})
        self.filtered(lambda x: x.state == 'draft').write({'state': 'confirmed'})
        return True
    
        
    
    def action_cancel(self):
        self.ensure_one()
        for invoice in self.invoice_ids:
            invoice.write({'counter_receipt_id' : False,
                           'invoice_date_due'           : invoice.original_date_due,
                           'original_date_due'  : False})
            for ml in invoice.line_ids.filtered(lambda x: x.account_id.internal_type in ('receivable', 'payable')):
                ml.write({'date_maturity' : ml.original_date_maturity or ml.date_maturity, 'original_date_maturity' : False})
        #self.write({'state':'cancel', 'invoice_m2m_ids':[(5, 0, 0)]})
        self.write({'state':'cancel'})
        return True
    

    
    def action_print_document(self):        
        return self.env.ref('account_invoice_counter_receipt.action_report_account_invoice_counter_receipt')\
            .with_context({'discard_logo_check': True}).report_action(self)
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
