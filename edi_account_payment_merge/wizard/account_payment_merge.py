# -*- encoding: utf-8 -*-   

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

import re

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    merged = fields.Boolean('Fusionado')

    payment_invoice_line_ids = fields.One2many('account.payment.invoice', 'payment_id', 'Desglose Facturas Pagadas', readonly=True)

    def group_moves_data_in_payment(self, main_payment, main_move):
        account_move_lines_groupped_credit = []
        account_move_lines_groupped_debit = []
        finally_amount_groupped_credit = 0.0
        finally_amount_groupped_debit = 0.0
        finally_amount_currency_credit = 0.0
        finally_amount_currency_debit = 0.0
        destination_account_id = main_payment.destination_account_id.id
        destination_journal_id = main_payment.journal_id.id

        account_journal_id = False

        payment_credit_account_id = main_payment.journal_id.outbound_payment_method_line_ids.payment_account_id
        payment_debit_account_id = main_payment.journal_id.inbound_payment_method_line_ids.payment_account_id

        # payment_credit_account_id = main_payment.company_id.account_journal_payment_credit_account_id
        # payment_debit_account_id = main_payment.company_id.account_journal_payment_debit_account_id

        if main_payment.payment_type == 'outbound':
            account_journal_id = payment_credit_account_id
        elif main_payment.payment_type == 'inbound':
            account_journal_id = payment_debit_account_id

        if not account_journal_id:
            _logger.info("\n:::::: Error al Agrupar. No se pudo obtener la cuenta del diario %s " % main_payment.journal_id.name)
            return True
        cr = self.env.cr
        cr.execute("""
            select id, credit, amount_currency from account_move_line where account_id = %s
                and move_id = %s
                and credit > 0.0;
            """, (account_journal_id, main_move.id))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            account_move_lines_groupped_credit = [x[0] for x in cr_res]
            for lmove in cr_res:
                finally_amount_groupped_credit += lmove[1]
                finally_amount_currency_credit += lmove[2]
        cr.execute("""
            select id, debit, amount_currency from account_move_line where account_id = %s
                and move_id = %s
                and debit > 0.0;
            """, (account_journal_id, main_move.id))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            account_move_lines_groupped_debit = [x[0] for x in cr_res]
            for lmove in cr_res:
                finally_amount_groupped_debit += lmove[1]
                finally_amount_currency_debit += lmove[2]

        if not account_move_lines_groupped_credit and not account_move_lines_groupped_debit:
            _logger.info("\n:::: No hay nada que agrupar >>> ")
            return True
        _logger.info("\n:::: finally_amount_currency_credit >>> %s " % finally_amount_currency_credit)
        _logger.info("\n:::: finally_amount_currency_debit >>> %s " % finally_amount_currency_debit)

        len_credit_grouped = len(account_move_lines_groupped_credit)
        line_credit_grouped_first = account_move_lines_groupped_credit[0] if account_move_lines_groupped_credit else False
        len_debit_grouped = len(account_move_lines_groupped_debit)
        line_debit_grouped_first = account_move_lines_groupped_debit[0] if account_move_lines_groupped_debit else False
        ### configuramos las partidas a eliminar sin la linea 0 ###
        if account_move_lines_groupped_credit:
            account_move_lines_groupped_credit.pop(0)
        if account_move_lines_groupped_debit:
            account_move_lines_groupped_debit.pop(0)
        group_something = False
        if len_credit_grouped > 1:
            group_something = True
        if len_debit_grouped > 1:
            group_something = True
        if not group_something:
            _logger.info("\n:::: No hay nada que agrupar >>> ")
            return True

        ### AQUI CONTINUAMOS CON LA ELIMINACION DE LAS PARTIDAS ####
        ### Creditos #####
        if account_move_lines_groupped_credit:
            _logger.info("\n:::: Credit - Borrando el AML ID %s >>> " % account_move_lines_groupped_credit)
            cr.execute("""
                delete from account_move_line where id in %s;
                """,(tuple(account_move_lines_groupped_credit), ))
        ### Debitos #####
        if account_move_lines_groupped_debit:
            _logger.info("\n:::: Debit - Borrando el AML ID %s >>> " % account_move_lines_groupped_debit)
            cr.execute("""
                delete from account_move_line where id in %s;
                """,(tuple(account_move_lines_groupped_debit), ))
        if line_credit_grouped_first:
            _logger.info("\n:::: Credit - Update %s >>>>>>>>> " % line_credit_grouped_first)
            cr.execute("""
                update account_move_line set credit = %s, amount_currency = %s where id = %s;
                """,(finally_amount_groupped_credit, finally_amount_currency_credit, line_credit_grouped_first, ))
            # cr.execute("""
            #     update account_move_line set amount_currency = %s where id = %s;
            #     """,(finally_amount_currency_credit, line_credit_grouped_first, ))
        if line_debit_grouped_first:
            _logger.info("\n:::: Debit - Update %s >>>>>>>>> " % line_debit_grouped_first)
            cr.execute("""
                update account_move_line set debit = %s, amount_currency = %s where id = %s;
                """,(finally_amount_groupped_debit, finally_amount_currency_debit, line_debit_grouped_first, ))
            # cr.execute("""
            #     update account_move_line set amount_currency = %s where id = %s;
            #     """,(finally_amount_currency_debit, line_debit_grouped_first, ))

class AccountPaymentMerge(models.TransientModel):
    _name = 'account.payment.merge'
    _description = 'Wizard para Fusionar Pagos'
    
    
    payment_ids = fields.Many2many('account.payment', string="Pagos a fusionar")


    @api.model
    def default_get(self, default_fields):
        res = super(AccountPaymentMerge, self).default_get(default_fields)
        active_ids = self._context.get('active_ids', [])
        res.update(payment_ids=[(6, 0, active_ids)])
        journal, payment_date, currency, partner = False, False, False, False
        for payment in self.env['account.payment'].browse(active_ids):
            if payment.merged:
                raise UserError("Este pago ya fue fusionado anteriormente.")
            #if not (payment.payment_type == 'inbound' and payment.partner_type=='customer'):
            #    raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos que no sean de Pagos de Clientes (Pago: %s)") % payment.name)
            
            if not payment.reconciled_invoices_count:
                raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos si no tiene Facturas asociadas (Pago: %s)") % payment.name)
            # Revisamos que sea la misma Empresa
            if partner and partner != payment.partner_id.id:
                raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos con diferente Empresa"))
            else:
                partner = payment.partner_id.id
            # Revisamos Diario de Pago
            if journal and journal != payment.journal_id.id:
                raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos con diferente Diario de Pago"))
            else:
                journal = payment.journal_id.id
            # Revisamos Fecha de Pago
            if payment_date and payment_date != payment.date:
                raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos con diferente Fecha de Pago"))
            else:
                payment_date = payment.date
            # Revisamos Moneda de Pago
            if currency and currency != payment.currency_id.id:
                raise ValidationError(_("Advertencia!!!\nNo puede fusionar pagos con diferente Moneda"))
            else:
                currency = payment.currency_id.id
            # Revisamos que no tenga Timbre
            if payment.l10n_mx_edi_cfdi_uuid:
                raise ValidationError(_("Advertencia !!!\nNo puede fusionar Pagos si ya se encuentran con Timbre Fiscal (Pago: %s)") % payment.name)
            if payment.state != 'posted':
                raise ValidationError(_("Advertencia !!!\nNo puede fusionar Pagos si NO se encuentran Confirmados (Pago: %s)") % payment.name)
            
        return res

    def create_payment_invoice_references(self, main_payment, payments_instance):
        payment_line_obj = self.env['account.payment.invoice']
        invoice_obj = self.env['account.move']
        for payment in payments_instance:
            invoices_related_to_payment = payment.reconciled_invoice_ids
            if not invoices_related_to_payment:
                invoices_related_to_payment = invoice_obj.search([('payment_id','=',payment.id)])
            for invoice in invoices_related_to_payment.sorted(key=lambda x: (x.invoice_date_due, x.name)):
                monto_aplicado = 0.0 
                data = {'payment_id': main_payment.id,
                        'invoice_id': invoice.id,
                       }
                monto_pago = 0.0
                for xline in payment.move_id.line_ids:
                    for r in xline.matched_debit_ids:
                        _logger.info("=====================")
                        for x in r._fields:
                            _logger.info("%s: %s" % (x, r[x]))
                        if r.debit_move_id.move_id.id == invoice.id:
                            if invoice.currency_id == invoice.company_id.currency_id == payment.currency_id:
                                monto_pago = r.amount
                            elif (invoice.company_id.currency_id == payment.currency_id and \
                                invoice.currency_id != invoice.company_id.currency_id) or \
                                invoice.currency_id == payment.currency_id:
                                monto_pago = r.debit_amount_currency
                            else:
                                monto_pago = invoice.company_id.currency_id.with_context({'date': invoice.date_invoice}).compute(r.amount, invoice.currency_id)
                last_data = {}
                _logger.info("monto_pago: %s" % monto_pago)
                if monto_pago:
                    ##########
                    pagos = invoice._get_reconciled_info_JSON_values()
                    _logger.info("pagos: %s" %  pagos)
                    for xdata in pagos:
                        _logger.info("data: %s" % xdata)    
                    
                    saldo_anterior = invoice.amount_residual + monto_pago
                    data.update({'parcialidad'  : len(invoice._get_reconciled_payments().filtered(lambda p: p.state not in ('draft', 'cancelled') and not p.move_id.line_ids.mapped('move_id.reversed_entry_id')).ids),
                                'saldo_anterior': saldo_anterior,
                                'monto_pago'    : monto_pago,
                                })
                    xres = payment_line_obj.create(data)
        return True

    def merge_payments(self):
        # account_payment_invoice_obj = self.env['account.payment.invoice']
        active_ids = self._context.get('active_ids', [])
        payments_brs = self.env['account.payment'].browse(active_ids)
        main_payment = self.payment_ids[0]
        main_move = main_payment.move_id
        payment_reference = main_payment.payment_reference
        amount = main_payment.amount
        factoraje = 0.0
        _logger.info("factoraje: %s" % factoraje)
        self.create_payment_invoice_references(main_payment, self.payment_ids)
        for payment in self.payment_ids:
            if main_payment == payment:
                continue
            _logger.info("Procesando el pago: %s" % payment.name)
            amount += payment.amount
            # factoraje += 'monto_factoraje_financiero' in payment._fields and payment.monto_factoraje_financiero or 0.0
            # if 'monto_factoraje_financiero' in main_payment._fields:
            #     _logger.info("payment.monto_factoraje_financiero: %s" % payment.monto_factoraje_financiero)
            # else:
            #     _logger.info("El registro %s no contiene Factoraje Financiero (payment.monto_factoraje_financiero)" % payment.name)
            move = payment.move_id

            # account_payment_invoice_ids = payment.payment_invoice_line_ids
            payment_move_line_ids = payment.move_id.line_ids.ids
            _logger.info("\n:::: payment_move_line_ids %s >>>>>>>>> " % payment_move_line_ids)
            
            query = """
            update account_move_line set move_id=%s, payment_id=%s where id in %s;
            delete from account_move where id=%s;
            """ % (main_move.id, main_payment.id, tuple(payment.move_id.line_ids.ids), move.id)
            #_logger.info("query: %s" % query)
            self._cr.execute(query)
            payment.state = 'cancel'
            # payment.payment_invoice_line_ids.write({'payment_id': main_payment.id})
            if payment.payment_reference:
                if payment_reference:
                    payment_reference += ' : ' + payment.payment_reference
                else:
                    payment_reference = payment.payment_reference
        ### Recorriendo los Pagos  - Agrupando la cuenta de Bancos###
        self.payment_ids.group_moves_data_in_payment(main_payment,main_move)
        xdata = {'amount' : amount, 'payment_reference' : payment_reference, 'merged': True}
        # _logger.info("factoraje: %s" % factoraje)
        # if 'monto_factoraje_financiero' in main_payment._fields and factoraje:
        #     xdata['monto_factoraje_financiero'] = factoraje
        _logger.info("xdata: %s" % xdata)
        for fieldname in xdata.keys():
            fieldvalue = xdata[fieldname]
            self.env.cr.execute("""
                update account_payment set %s=%s where id =%s;
                """ % (fieldname, fieldvalue, main_payment.id))
        #main_payment.write(xdata)

        return {
            'domain': "[('id','in', ["+','.join(map(str,[main_payment.id]))+"])]",
            'name': _('Pagos'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'view_id': False,
            'context': "{'create':False}",
            'type': 'ir.actions.act_window'
        }



class AccountPaymentInvoice(models.Model):
    _name = 'account.payment.invoice'
    _description="Parcialidades pagadas a facturas (para CFDI Pagos)"

    @api.depends('invoice_id', 'payment_id')
    def _get_currency_rate(self):
        for rec in self:
            if not rec.invoice_id or rec.invoice_id.currency_id == rec.env.user.company_id.currency_id:
                rec.invoice_currency_rate = 1.0
                return
            rec.invoice_currency_rate = round(1.0 / rec.invoice_id.currency_id.with_context({'date': rec.payment_date}).compute(1, rec.currency_id, round=False), 6)
        #if self.payment_currency_id == self.env.user.company_id.currency_id:
        #    self.invoice_currency_rate = abs(self.invoice_id.amount_total_signed / self.invoice_id.amount_total_company_signed)
        #else:
        #    self.invoice_currency_rate = abs(self.invoice_id.amount_total_company_signed / self.invoice_id.amount_total_signed)
     
    
    @api.depends('saldo_anterior', 'monto_pago')
    def _get_saldo_final(self):
        for rec in self:
            rec.saldo_final = round(rec.saldo_anterior - rec.monto_pago, 2)

    @api.depends('invoice_id')
    def _l10n_mx_edi_get_serie_and_folio(self,):
        for rec in self:
            name_numbers = list(re.finditer('\d+', rec.name))
            serie_number = rec.name[:name_numbers[-1].start()]
            folio_number = name_numbers[-1].group().lstrip('0')
            rec.invoice_serie = serie_number
            rec.invoice_folio = folio_number

    name = fields.Char('Descripcion Factura', related="invoice_id.name")
    payment_id  = fields.Many2one('account.payment', 'Pago', required=True)
    payment_state = fields.Selection(string="Estado", readonly=True, related="payment_id.state")
    payment_currency_id = fields.Many2one('res.currency', string="Moneda de Pago", related='payment_id.currency_id', readonly=True)
    currency_id = fields.Many2one('res.currency', string="Moneda", related='payment_id.currency_id', readonly=True)
    payment_date = fields.Date(string="Fecha Pago", related='payment_id.date', readonly=True)
    payment_amount = fields.Monetary(string="Monto Pago", related='payment_id.amount', readonly=True)
    
    invoice_id  = fields.Many2one('account.move', string='Factura', required=True)
    invoice_serie = fields.Char(string='Serie', readonly=True, compute="_l10n_mx_edi_get_serie_and_folio")
    invoice_folio = fields.Char(string='Folio', readonly=True, compute="_l10n_mx_edi_get_serie_and_folio")
    invoice_uuid = fields.Char(related='invoice_id.l10n_mx_edi_cfdi_uuid', string='Folio Fiscal', readonly=True)
    invoice_currency_id = fields.Many2one('res.currency', string="Moneda Factura", related='invoice_id.currency_id', readonly=True)
    invoice_currency_rate = fields.Float(compute='_get_currency_rate', digits=(22, 16), readonly=True)
    
    parcialidad = fields.Integer('Parcialidad', default=1, required=True)
    saldo_anterior = fields.Float('Saldo Anterior', default=0.0, help="Saldo Anterior (en Moneda de la Factura)")
    monto_pago  = fields.Float('Monto Aplicado', default=0.0, help="Monto Pago (en Moneda de la Factura)")
    saldo_final = fields.Float('Saldo Insoluto', compute='_get_saldo_final', store=True,
                               help="Saldo Insoluto (en Moneda de la Factura) después del pago")


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _l10n_mx_edi_get_common_cfdi_values(self, move):
        res = super(AccountEdiFormat, self)._l10n_mx_edi_get_common_cfdi_values(move)
        context = self._context
        if move.payment_id:
            res.update({
                        'payment_invoice_line_ids': move.payment_id.payment_invoice_line_ids,
                    })
        return res

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    def _check_reconciliation(self):
        context = self._context
        if context.get('no_check_move',False):
            return True
        for line in self:
            if line.matched_debit_ids or line.matched_credit_ids:
                raise UserError(_("You cannot do this modification on a reconciled journal entry. "
                                  "You can just change some non legal fields or you must unreconcile first.\n"
                                  "Journal Entry (id): %s (%s)") % (line.move_id.name, line.move_id.id))

