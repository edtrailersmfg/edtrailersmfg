# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero, pycompat
#import json
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    
    def assign_outstanding_credit(self, credit_aml_id):
        self.ensure_one()
        invoice = self
        credit_aml = self.env['account.move.line'].browse(credit_aml_id)
        aml_to_reconcile = False

        # Revisamos si se requiere poliza para reclasificar el Anticipo de Cliente
        if (invoice.type == 'in_invoice' and \
            credit_aml.account_id.id != invoice.partner_id.property_account_payable_id.id and \
            credit_aml.account_id.id == (invoice.partner_id.property_account_supplier_advance_id and invoice.partner_id.property_account_supplier_advance_id.id or False)) \
           or \
            (invoice.type == 'out_invoice' and \
            credit_aml.account_id.id != credit_aml.partner_id.property_account_receivable_id.id and \
            credit_aml.account_id.id == (credit_aml.partner_id.property_account_customer_advance_id and credit_aml.partner_id.property_account_customer_advance_id.id or False)):

            if (invoice.type == 'out_invoice' and not invoice.partner_id.property_account_customer_advance_id) or\
               (invoice.type == 'in_invoice' and not invoice.partner_id.property_account_supplier_advance_id):
                raise UserError(_('The Partner has no Account defined for Customer / Supplier Advance Application. Please check.'))

            aml_obj = self.env['account.move.line']
            move_obj = self.env['account.move']
            #available_advance_amount_company_curr = credit_aml.amount_residual
            if credit_aml.currency_id: # Anticipo en ME
                if credit_aml.currency_id == invoice.currency_id: # Moneda Anticipo == Moneda Factura
                    available_advance_amount_invoice_curr = credit_aml.amount_residual_currency
                else: # Moneda Anticipo != Moneda Factura
                    available_advance_amount_invoice_curr = credit_aml.currency_id.with_context(date=credit_aml.date).compute(abs(credit_aml.amount_residual_currency), invoice.currency_id)
            elif invoice.currency_id == invoice.company_id.currency_id: # Moneda Anticipo MN == Moneda Factura MN
                available_advance_amount_invoice_curr = credit_aml.amount_residual
            elif invoice.currency_id != invoice.company_id.currency_id: #  Moneda Anticipo MN, Moneda Factura ME
                available_advance_amount_invoice_curr = credit_aml.company_id.currency_id.with_context(date=credit_aml.date).compute(abs(credit_aml.amount_residual), invoice.currency_id)

            if float_is_zero(available_advance_amount_invoice_curr, precision_rounding=invoice.currency_id.rounding):
                available_advance_amount_invoice_curr = 0.0

            # Calculamos el porcentaje del Anticipo a aplicar a la factura
            factor = available_advance_amount_invoice_curr and (invoice.residual / available_advance_amount_invoice_curr) or 0.0
            if abs(factor) > 1.0: 
                factor = 1.0 * (available_advance_amount_invoice_curr >= 0 and 1 or -1)

            advance_amount_mn = abs(factor * credit_aml.amount_residual)
            advance_currency = False
            if credit_aml.currency_id:
                advance_amount_me = abs(factor * credit_aml.amount_residual_currency)
                advance_currency = credit_aml.currency_id
            else:
                advance_amount_me = 0.0
                if invoice.currency_id != invoice.company_id.currency_id:
                    advance_amount_me = credit_aml.company_id.currency_id.with_context(date=credit_aml.date).compute(abs(credit_aml.amount_residual), invoice.currency_id)
                    advance_currency = invoice.currency_id


            journal_id = self.env['account.journal'].search([('advance_application_journal','=',1)], limit=1)
            if not journal_id:
                raise UserError(_('There is no Journal defined for Customer / Supplier Advance Application. Please check.'))

            move_dict = {
                'date'      : fields.Date.context_today(self),
                'ref'       : _('Pre-paid Application to Invoice: %s') % ((invoice.type=='out_invoice' and invoice.number or invoice.reference)),
                'narration' : _('Pre-paid Application to Invoice: %s') % ((invoice.type=='out_invoice' and invoice.number or invoice.reference)),
                'company_id': invoice.company_id.id,
                'journal_id': journal_id.id,
                }
            # Creamos la partida para la cuenta de Cliente / Proveedor
            aml_dict_partner = credit_aml.copy_data()[0]
            aml_dict_partner.update({
                'name'           : _('Pre-paid Application to Invoice: %s') % (invoice.reference or invoice.number),
                'account_id'     : invoice.account_id.id,
                'date_maturity'  : fields.Date.context_today(self),
                'debit'          : invoice.type=='in_invoice' and advance_amount_mn or 0,
                'credit'         : invoice.type=='out_invoice' and advance_amount_mn or 0,
                'currency_id'    : advance_currency and advance_currency.id or False,
                'amount_currency': (advance_amount_me and ((invoice.type=='in_invoice' and advance_amount_me) or (invoice.type=='out_invoice' and -advance_amount_me) or False)) or False,
                'partner_id'     : invoice.partner_id.id,
            })
            aml_dict_advance = aml_dict_partner.copy()
            aml_dict_advance.update({
                'account_id': (invoice.type=='in_invoice' and invoice.partner_id.property_account_supplier_advance_id.id) or \
                              (invoice.type=='out_invoice' and invoice.partner_id.property_account_customer_advance_id.id),
                'debit'     : aml_dict_partner['credit'],
                'credit'    : aml_dict_partner['debit'],
                'amount_currency': aml_dict_partner['amount_currency'] and -aml_dict_partner['amount_currency'] or 0.0,
            })
            ###################################################
            ###################################################
            fc_currency_id = credit_aml.currency_id and credit_aml.currency_id.id or credit_aml.company_id.currency_id.id
            lines = []
            factor_base = available_advance_amount_invoice_curr and (available_advance_amount_invoice_curr / invoice.residual) or 0.0
            factor_base2 = available_advance_amount_invoice_curr and (available_advance_amount_invoice_curr / invoice.amount_total) or 0.0
            if abs(factor_base) > 1.0:
                factor_base = 1.0
                factor_base2 = invoice.residual / invoice.amount_total
            for inv_line_tax in invoice.tax_line_ids.filtered(lambda r: r.tax_id.use_tax_cash_basis==True):
                src_account_id = inv_line_tax.tax_id.account_id.id
                dest_account_id = inv_line_tax.tax_id.tax_cash_basis_account.id
                if not (src_account_id and dest_account_id):
                    raise UserError(_("Tax %s is not properly configured, please check." % (inv_line_tax.tax_id.name)))
                for move_line in invoice.move_id.line_ids:
                    if move_line.account_id.id == inv_line_tax.tax_id.account_id.id:
                        mi_company_curr_orig = (move_line.debit + move_line.credit) * factor_base2 * (inv_line_tax.tax_id.amount >= 0 and 1.0 or -1.0)
                        mib_company_curr_orig = round(move_line.amount_base * factor_base2, 2)
                #mi_invoice = inv_line_tax.amount * factor_base2
                #mib_invoice = mib_company_curr_orig / (mi_company_curr_orig / mi_invoice)
                #################################
                if ((invoice.type=='out_invoice' and inv_line_tax.tax_id.amount >= 0.0) or \
                             (invoice.type=='in_invoice' and inv_line_tax.tax_id.amount < 0.0)):
                    debit = round(abs(mi_company_curr_orig),2)
                    credit = 0
                elif ((invoice.type=='in_invoice' and inv_line_tax.tax_id.amount >= 0.0) or \
                             (invoice.type=='out_invoice' and inv_line_tax.tax_id.amount < 0.0)):
                    debit = 0
                    credit = round(abs(mi_company_curr_orig),2)

                #################################
                line2 = {
                        'name'            : inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                        'partner_id'      : invoice.partner_id.id, 
                        'debit'           : debit,
                        'credit'          : credit,
                        'account_id'      : src_account_id, 
                        'tax_id_secondary': inv_line_tax.tax_id.id,
                        'analytic_account_id': False,
                        'amount_base'     : abs(mib_company_curr_orig),
                    }

                line1 = line2.copy()
                line3 = {}
                xparam = self.env['ir.config_parameter'].get_param('tax_amount_according_to_currency_exchange_on_payment_date')[0]
                if not xparam == "1" or (invoice.company_id.currency_id.id == fc_currency_id == invoice.currency_id.id):
                    line1.update({
                        'name'        : inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                        'account_id'  : dest_account_id,
                        'debit'       : line2['credit'],
                        'credit'      : line2['debit'],
                        'amount_base' : line2['amount_base'],
                        })
                elif xparam == "1":
                    monto_base = round((inv_line_tax.tax_id.amount and advance_amount_mn \
                                                / (1.0 + (inv_line_tax.tax_id.amount / 100)) or (factor_base2 * inv_line_tax.amount_base_company_curr)), 2)
                    monto_a_reclasificar = round(inv_line_tax.tax_id.amount and monto_base * (inv_line_tax.tax_id.amount / 100) or 0.0,2)

                    line1.update({
                        'name': inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                        'debit': line2['credit'] and abs(monto_a_reclasificar) or 0.0,
                        'credit': line2['debit'] and abs(monto_a_reclasificar) or 0.0,
                        'account_id': dest_account_id,
                        'amount_base' : abs(monto_base),
                        })

                    if (round(mi_company_curr_orig, 2) - round(monto_a_reclasificar,2)):
                        amount_diff =  (round(abs(mi_company_curr_orig),2) - round(abs(monto_a_reclasificar),2)) * \
                                        (inv_line_tax.tax_id.amount >= 0 and 1.0 or -1.0)
                        line3 = {
                            'name': _('Diferencia de ') + inv_line_tax.tax_id.name + (invoice and (_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                            'partner_id': invoice.partner_id.id,
                            'debit': ((amount_diff < 0 and invoice.type=='out_invoice') or (amount_diff >= 0 and invoice.type=='in_invoice')) and abs(amount_diff) or 0.0,
                            'credit': ((amount_diff < 0 and invoice.type=='in_invoice') or (amount_diff >= 0 and invoice.type=='out_invoice')) and abs(amount_diff) or 0.0,
                            'account_id': (amount_diff < 0 ) and invoice.company_id.income_currency_exchange_account_id.id or invoice.company_id.expense_currency_exchange_account_id.id,
                            'analytic_account_id': False,
                            }
                    #else:
                    #    line3 = {}
                lines += line3 and [(0,0,line1),(0,0,line2),(0,0,line3)] or [(0,0,line1),(0,0,line2)]
            lines += [(0,0, aml_dict_partner),(0,0, aml_dict_advance)] 

            #for line in lines:
            #    print "line: ", line
            #raise UserError('Pausa')   
            ###################################################
            ###################################################
            move_dict.update({'line_ids': lines})

            move = move_obj.create(move_dict)
            move.post()
            aml_to_reconcile_advance = move.line_ids[0]
            # Creamos la partida para "descargar" la cuenta de Anticipo de Cliente / Proveedor
            aml_to_reconcile = move.line_ids[1]
            (aml_to_reconcile_advance + credit_aml).reconcile()

        if aml_to_reconcile: # Se aplico Anticipo
            return self.register_payment(aml_to_reconcile)
        else:
            if not credit_aml.currency_id and invoice.currency_id != invoice.company_id.currency_id:
                credit_aml.with_context(allow_amount_currency=True).write({
                    'amount_currency': invoice.company_id.currency_id.with_context(date=credit_aml.date).compute(credit_aml.balance, invoice.currency_id),
                    'currency_id': invoice.currency_id.id})
            if credit_aml.payment_id:
                credit_aml.payment_id.write({'invoice_ids': [(4, self.id, None)]})
            return invoice.register_payment(credit_aml)   



class AccountPayment(models.Model):
    _inherit = "account.payment"

    
    def action_post(self):
        super(AccountPayment, self).action_post()
        _logger.info("reconciled_invoice_ids: %s" % self.reconciled_invoice_ids)
        _logger.info("reconciled_bill_ids: %s" % self.reconciled_bill_ids)
        
        
    def argil_create_move_line(self, move_id, line):
        sql = ""
        for l in line:
            l[2].update({'payment_id':self.id})
            sql_insert, sql_valores = "", ""
            for key, valor in l[2].items():
                sql_insert += "%s,\n" % (key)
                sep = not (type(valor) is float or type(valor) is int)
                sql_valores += "%s,\n" % (valor is not False and ((sep and "'%s'" or "%s") % (valor)) or 'null')

            sql += "insert into account_move_line (" + sql_insert + "create_uid, write_uid, create_date, write_date) values (" + sql_valores + \
                        ("%s,%s,%s,%s" % (self._uid, self._uid,"(now() at time zone 'UTC')", "(now() at time zone 'UTC')")) + ");"
        self._cr.execute(sql)
        return
    
    
    def _create_payment_entry(self, amount):
        move = super(AccountPayment, self)._create_payment_entry(amount)
        _logger.info("argil_account_tax_cash_basis._create_payment_entry(amount)")
        _logger.info("move: %s" % move)
        tax_lines_dict = self._get_tax_paid_basis_entries(move)
        if tax_lines_dict:
            aml_obj = self.env['account.move.line']
            move.button_cancel()
            for l in tax_lines_dict:
                aml_obj.with_context(check_move_validity=False).create(l[2])
            move.post()
        return move


        
    def _get_tax_paid_basis_entries(self, move):
        """ Reconcile payable/receivable lines from the invoice with payment_line """
        if not self.invoice_ids:
            return []
        active_ids = self.invoice_ids.ids
        
        currency_obj = self.env['res.currency']
        invoice_obj = self.env['account.move']
        
        move_id = move.id
        company_currency_id = self.company_id.currency_id
        payment_currency_id = self.currency_id or company_currency_id
        
        payment_amount_company_curr = self.move_line_ids[0].debit + self.move_line_ids[0].credit
        payment_amount_original_curr = self.amount
        invoice_currency_id = self.invoice_ids[0].currency_id
        currency_flag = False
        if company_currency_id.id == payment_currency_id.id == invoice_currency_id.id: # Invoice(s) & Payment in Company Currency
            payment_amount = payment_amount_company_curr
            currency_flag = True
        elif company_currency_id.id != payment_currency_id.id and payment_currency_id.id == invoice_currency_id.id: # Same Currency for Payment & Invoice(s) but not in company Currency
            payment_amount = payment_amount_original_curr
        else: # Payment, Invoice(s) and Company Currency not equal from each other            
            payment_amount = payment_currency_id.with_context(date=self.payment_date).compute(payment_amount_original_curr, invoice_currency_id)
        invoice_ids = active_ids #[x.id for x in self.invoice_ids]
        invoices_grouped = {}
        try:
            self._cr.execute("""
                    drop table if exists borrame_partidas;
                    select aml.id
                    into borrame_partidas
                    from account_move_line aml
                    inner join account_account aa on aa.id=aml.account_id and aa.internal_type in ('payable', 'receivable')
                    where payment_id=%s;
                    select ai.id, apr.amount, apr.amount_currency, apr.currency_id, aml.date_maturity
                    from account_partial_reconcile apr
                    inner join account_move_line aml on aml.id <> (select id from borrame_partidas)
                                                        and (aml.id=apr.credit_move_id or aml.id=apr.debit_move_id)
                    inner join account_invoice ai on ai.move_id=aml.move_id
                    where (apr.credit_move_id=(select id from borrame_partidas) or 
                           apr.debit_move_id=(select id from borrame_partidas))
                    order by aml.date_maturity asc;
                """ % self.id)
        except:
            raise ValidationError(_("Advertencia !\nLa cuenta contable del Diario de Pago no está configurada correctamente, debe ser Tipo Bancos / Caja"))
        
        cr_res = self._cr.fetchall()
        sum_voucher_lines = 0.0
        for x in cr_res:
            
            val = {}
            val['invoice_id'], val['invoice_amount'], val['invoice_amount_currency'], val['invoice_currency_id'] = x[0], abs(x[1]), abs(x[2]), x[3]
            if not payment_amount:
                continue
            if payment_amount >= (currency_flag and val['invoice_amount'] or val['invoice_amount_currency']):
                #### Modificación Correccion de Reclasificacion Pagando facturas en una moneda distinta ####
                if currency_flag and val['invoice_amount']:
                    amount_assigned = val['invoice_amount']
                else:
                    if val['invoice_amount_currency']:
                        amount_assigned = val['invoice_amount_currency']
                    else:
                        amount_assigned = val['invoice_amount']
                val['amount_assigned'] = amount_assigned
                payment_amount = payment_amount - amount_assigned
            elif payment_amount and payment_amount < (currency_flag and val['invoice_amount'] or val['invoice_amount_currency']):
                val['amount_assigned'] = payment_amount
                payment_amount = 0.0
            else:
                val['amount_assigned'] = 0.0
            key = (val['invoice_id'],val['invoice_currency_id'])
            sum_voucher_lines += val['invoice_amount']
            if not key in invoices_grouped:
                invoices_grouped[key] = val
            else:
                invoices_grouped[key]['invoice_amount'] += val['invoice_amount']
                invoices_grouped[key]['invoice_amount_currency'] += val['invoice_amount_currency']
                invoices_grouped[key]['amount_assigned'] += val['amount_assigned']
            
        precision = self.env['decimal.precision'].precision_get('Account')
        journal_id = self.journal_id.id
        date = self.payment_date
        currency_obj = self.env['res.currency']
        res = []
        for inv in invoices_grouped.values():
            factor_base = sum_voucher_lines and inv['invoice_amount'] / sum_voucher_lines or 0.0
            for invoice in invoice_obj.browse([inv['invoice_id']]):
                factor = inv['amount_assigned'] / invoice.amount_total
                for inv_line_tax in invoice.tax_line_ids.filtered(lambda r: r.tax_id.use_tax_cash_basis==True):
                    #_logger.info("\n------------------------------\nImpuesto: %s" % inv_line_tax.tax_id.name)
                    src_account_id = inv_line_tax.tax_id.account_id.id
                    dest_account_id = inv_line_tax.tax_id.tax_cash_basis_account.id
                    if not (src_account_id and dest_account_id):
                        raise UserError(_("Tax %s is not properly configured, please check." % (inv_line_tax.tax_id.name)))
                    mib_company_curr_orig, mi_company_curr_orig = 0.0, 0.0
                    for move_line in invoice.move_id.line_ids:
                        if move_line.account_id.id == inv_line_tax.tax_id.account_id.id and \
                            move_line.tax_id_secondary.id == inv_line_tax.tax_id.id:
                            mi_company_curr_orig = (move_line.debit + move_line.credit) * factor
                            mib_company_curr_orig = move_line.amount_base * factor
                    if not mib_company_curr_orig and not inv_line_tax.tax_id.amount:
                        mib_company_curr_orig = inv_line_tax.amount_base_company_curr
                    #mi_invoice = inv_line_tax.amount * factor
                    #mib_invoice = mib_company_curr_orig / (mi_company_curr_orig / mi_invoice)                    
                    #################################
                    debit, credit = 0.0, 0.0
                    if ((invoice.type=='out_invoice' and inv_line_tax.tax_id.amount >= 0.0) or \
                                 (invoice.type=='in_invoice' and inv_line_tax.tax_id.amount < 0.0)):
                        debit = round(abs(mi_company_curr_orig),2) or 0.0
                        credit = 0.0
                        #amount_currency = (company_currency_id.id != invoice.currency_id.id) and abs(mi_invoice) or False
                    elif ((invoice.type=='in_invoice' and inv_line_tax.tax_id.amount >= 0.0) or \
                                 (invoice.type=='out_invoice' and inv_line_tax.tax_id.amount < 0.0)):
                        debit = 0.0
                        credit = round(mi_company_curr_orig,2) or 0.0
                        #amount_currency = (company_currency_id.id != invoice.currency_id.id) and -abs(mi_invoice) or False
                    #################################
                    line2 = {
                            'name'            : inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                            'quantity'        : 1,
                            'product_uom_id'  : False,
                            'partner_id'      : invoice.partner_id.id, 
                            'debit'           : debit,
                            'credit'          : credit,
                            'account_id'      : src_account_id, 
                            'journal_id'      : journal_id,
                            'period_id'       : move.period_id.id,
                            'company_id'      : invoice.company_id.id,
                            'move_id'         : move.id,
                            'tax_id_secondary': inv_line_tax.tax_id.id,
                            'analytic_account_id': False,
                            'date'            : date,
                            'date_maturity'   : date,
                            'amount_base'     : mib_company_curr_orig,
                            'payment_id'      : self.id,
                        }
                    #_logger.info("line2: %s" % line2)
                    line1 = line2.copy()
                    line3 = {}
                    xparam = self.env['ir.config_parameter'].get_param('tax_amount_according_to_currency_exchange_on_payment_date')[0]
                    if not xparam == "1" or (company_currency_id.id == payment_currency_id.id == invoice.currency_id.id):
                        line1.update({
                            'name': inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                            'account_id'  : dest_account_id,
                            'debit'       : line2['credit'],
                            'credit'      : line2['debit'],
                            'amount_base' : line2['amount_base'],
                            #'amount_currency' : line2['amount_currency'] and -line2['amount_currency'] or False,
                            })
                    elif xparam == "1":
                        
                        xfactor = float(inv_line_tax.amount_base / invoice.amount_total)
                        monto_base = round(factor_base * (\
                                            (inv_line_tax.tax_id.amount and (payment_amount_company_curr * xfactor)) \
                                                          or inv_line_tax.amount_base_company_curr), 2) 

                        monto_a_reclasificar = round(inv_line_tax.tax_id.amount and monto_base * (inv_line_tax.tax_id.amount / 100) or 0.0,2)
                        
                        
                        line1.update({
                            'name': inv_line_tax.tax_id.name + ((_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                            'debit': line2['credit'] and abs(monto_a_reclasificar) or 0.0,
                            'credit': line2['debit'] and abs(monto_a_reclasificar) or 0.0,
                            'account_id': dest_account_id,
                            'amount_base' : abs(monto_base),
                            })
                        #_logger.info("line1: %s" % line1)
                        
                        if (round(mi_company_curr_orig, 2) - round(monto_a_reclasificar,2)):
                            amount_diff =  (round(abs(mi_company_curr_orig),2) - round(abs(monto_a_reclasificar),2)) * \
                                            (inv_line_tax.tax_id.amount >= 0 and 1.0 or -1.0)
                            amount_diff = round(amount_diff,2)
                            line3 = {
                                'name': _('Diferencia de ') + inv_line_tax.tax_id.name + (invoice and (_(" - Fact: ") + (invoice.type=='out_invoice' and invoice.number or invoice.reference)) or 'N/A'),
                                'quantity': 1,
                                'partner_id': invoice.partner_id.id,
                                'debit': ((amount_diff < 0 and invoice.type=='out_invoice') or (amount_diff >= 0 and invoice.type=='in_invoice')) and abs(amount_diff) or 0.0,
                                'credit': ((amount_diff < 0 and invoice.type=='in_invoice') or (amount_diff >= 0 and invoice.type=='out_invoice')) and abs(amount_diff) or 0.0,
                                'account_id': (amount_diff < 0 ) and inv_line_tax.tax_id.tax_cash_basis_account_diff_credit.id or inv_line_tax.tax_id.tax_cash_basis_account_diff_debit.id,
                                'journal_id': journal_id,
                                'period_id': move.period_id.id,
                                'company_id': invoice.company_id.id,
                                'move_id': move.id,
                                'analytic_account_id': False,
                                'date': date,
                                'date_maturity'   : date,
                                'currency_id': False,
                                'amount_currency' : False,
                                'payment_id'      : self.id,
                                }
                        else:
                            line3 = {}
                        #_logger.info("line3: %s" % line3)
                    lines = line3 and [(0,0,line1),(0,0,line2),(0,0,line3)] or [(0,0,line1),(0,0,line2)]
                    res += lines
                #for resx in res:
                #    _logger.info("resx: %s" % resx)
                #raise UserError('Pausa...')
        #raise UserError("### AQUI >>>>>>>> ")
        return res
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"    
    
    def process_reconciliation(self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        """ Match statement lines with existing payments (eg. checks) and/or payables/receivables (eg. invoices and credit notes) and/or new move lines (eg. write-offs).
            If any new journal item needs to be created (via new_aml_dicts or counterpart_aml_dicts), a new journal entry will be created and will contain those
            items, as well as a journal item for the bank statement line.
            Finally, mark the statement line as reconciled by putting the matched moves ids in the column journal_entry_ids.

            :param self: browse collection of records that are supposed to have no accounting entries already linked.
            :param (list of dicts) counterpart_aml_dicts: move lines to create to reconcile with existing payables/receivables.
                The expected keys are :
                - 'name'
                - 'debit'
                - 'credit'
                - 'move_line'
                    # The move line to reconcile (partially if specified debit/credit is lower than move line's credit/debit)

            :param (list of recordsets) payment_aml_rec: recordset move lines representing existing payments (which are already fully reconciled)

            :param (list of dicts) new_aml_dicts: move lines to create. The expected keys are :
                - 'name'
                - 'debit'
                - 'credit'
                - 'account_id'
                - (optional) 'tax_ids'
                - (optional) Other account.move.line fields like analytic_account_id or analytics_id

            :returns: The journal entries with which the transaction was matched. If there was at least an entry in counterpart_aml_dicts or new_aml_dicts, this list contains
                the move created by the reconciliation, containing entries for the statement.line (1), the counterpart move lines (0..*) and the new move lines (0..*).
        """
        counterpart_aml_dicts = counterpart_aml_dicts or []
        payment_aml_rec = payment_aml_rec or self.env['account.move.line']
        new_aml_dicts = new_aml_dicts or []

        aml_obj = self.env['account.move.line']

        company_currency = self.journal_id.company_id.currency_id
        statement_currency = self.journal_id.currency_id or company_currency
        st_line_currency = self.currency_id or statement_currency

        counterpart_moves = self.env['account.move']

        # Check and prepare received data
        if any(rec.statement_id for rec in payment_aml_rec):
            raise UserError(_('A selected move line was already reconciled.'))
        for aml_dict in counterpart_aml_dicts:
            if aml_dict['move_line'].reconciled:
                raise UserError(_('A selected move line was already reconciled.'))
            if isinstance(aml_dict['move_line'], pycompat.integer_types):
                aml_dict['move_line'] = aml_obj.browse(aml_dict['move_line'])
        for aml_dict in (counterpart_aml_dicts + new_aml_dicts):
            if aml_dict.get('tax_ids') and isinstance(aml_dict['tax_ids'][0], pycompat.integer_types):
                # Transform the value in the format required for One2many and Many2many fields
                aml_dict['tax_ids'] = [(4, id, None) for id in aml_dict['tax_ids']]
        if any(line.journal_entry_ids for line in self):
            raise UserError(_('A selected statement line was already reconciled with an account move.'))

            
        ###### ARGIL ###########################################################
        #################################################################
        # Revisamos si la partida a conciliar corresponde a una factura (para que aplique re-clasificacion de impuestos)
        total = self.amount
        xinvoice_ids = []
        for xl in counterpart_aml_dicts:
            if not xl['move_line'].invoice_id or not (abs(total)>0.00001 and self.partner_id.id == xl['move_line'].partner_id.id):
                continue
            xinvoice_ids.append(xl['move_line'].invoice_id.id)
        if xinvoice_ids: # Create The payment
            partner_id = self.partner_id and self.partner_id.id or False
            partner_type = False
            if partner_id:
                if total < 0:
                    partner_type = 'supplier'
                else:
                    partner_type = 'customer'

            payment_methods = (total>0) and self.journal_id.inbound_payment_method_ids or self.journal_id.outbound_payment_method_ids
            currency = self.journal_id.currency_id or self.company_id.currency_id
            payment = self.env['account.payment'].create({
                            'payment_method_id': payment_methods and payment_methods[0].id or False,
                            'payment_type': total >0 and 'inbound' or 'outbound',
                            'partner_id': self.partner_id and self.partner_id.id or False,
                            'partner_type': partner_type,
                            'journal_id': self.statement_id.journal_id.id,
                            'payment_date': self.date,
                            'state': 'draft',
                            'currency_id': currency.id,
                            'amount': abs(total),
                            'communication': self._get_communication(payment_methods[0] if payment_methods else False),
                            'name': self.statement_id.name,
                            'invoice_ids': [(4, xinv, None) for xinv in xinvoice_ids],
                        })
            payment.post()
            payment.write({'state': 'reconciled'})
            moves_to_assign_statement = payment.move_line_ids.filtered(lambda r: r.account_id.internal_type == 'liquidity')
            if not moves_to_assign_statement:
                raise ValidationError(_("Advertencia !\nLa cuenta contable del Diario de Pago no está configurada correctamente, debe ser Tipo Bancos / Caja"))
            moves_to_assign_statement.with_context(check_move_validity=False).write({'statement_id': self.statement_id.id})
            moves_to_assign_statement[0].move_id.write({'statement_line_id': self.id})
            payment_aml_rec = payment.move_line_ids.filtered(lambda r: r.account_id.internal_type in ('payable', 'receivable'))
            counterpart_aml_dicts = []

        #################################################################
        #################################################################
            
        # Fully reconciled moves are just linked to the bank statement
        total = self.amount
        for aml_rec in payment_aml_rec:
            total -= aml_rec.debit - aml_rec.credit
            aml_rec.with_context(check_move_validity=False).write({'statement_line_id': self.id})
            counterpart_moves = (counterpart_moves | aml_rec.move_id)

        # Create move line(s). Either matching an existing journal entry (eg. invoice), in which
        # case we reconcile the existing and the new move lines together, or being a write-off.
        if counterpart_aml_dicts or new_aml_dicts:
            st_line_currency = self.currency_id or statement_currency
            st_line_currency_rate = self.currency_id and (self.amount_currency / self.amount) or False

            # Create the move
            self.sequence = self.statement_id.line_ids.ids.index(self.id) + 1
            move_vals = self._prepare_reconciliation_move(self.statement_id.name)
            move = self.env['account.move'].create(move_vals)
            counterpart_moves = (counterpart_moves | move)

            # Create The payment
            payment = self.env['account.payment']
            if abs(total)>0.00001:
                partner_id = self.partner_id and self.partner_id.id or False
                partner_type = False
                if partner_id:
                    if total < 0:
                        partner_type = 'supplier'
                    else:
                        partner_type = 'customer'

                payment_methods = (total>0) and self.journal_id.inbound_payment_method_ids or self.journal_id.outbound_payment_method_ids
                currency = self.journal_id.currency_id or self.company_id.currency_id
                payment = self.env['account.payment'].create({
                    'payment_method_id': payment_methods and payment_methods[0].id or False,
                    'payment_type': total >0 and 'inbound' or 'outbound',
                    'partner_id': self.partner_id and self.partner_id.id or False,
                    'partner_type': partner_type,
                    'journal_id': self.statement_id.journal_id.id,
                    'payment_date': self.date,
                    'state': 'reconciled',
                    'currency_id': currency.id,
                    'amount': abs(total),
                    'communication': self._get_communication(payment_methods[0] if payment_methods else False),
                    'name': self.statement_id.name or _("Bank Statement %s") %  self.date,
                })

            # Complete dicts to create both counterpart move lines and write-offs
            to_create = (counterpart_aml_dicts + new_aml_dicts)
            ctx = dict(self._context, date=self.date)
            for aml_dict in to_create:
                aml_dict['move_id'] = move.id
                aml_dict['partner_id'] = self.partner_id.id
                aml_dict['statement_line_id'] = self.id
                if st_line_currency.id != company_currency.id:
                    aml_dict['amount_currency'] = aml_dict['debit'] - aml_dict['credit']
                    aml_dict['currency_id'] = st_line_currency.id
                    if self.currency_id and statement_currency.id == company_currency.id and st_line_currency_rate:
                        # Statement is in company currency but the transaction is in foreign currency
                        aml_dict['debit'] = company_currency.round(aml_dict['debit'] / st_line_currency_rate)
                        aml_dict['credit'] = company_currency.round(aml_dict['credit'] / st_line_currency_rate)
                    elif self.currency_id and st_line_currency_rate:
                        # Statement is in foreign currency and the transaction is in another one
                        aml_dict['debit'] = statement_currency.with_context(ctx).compute(aml_dict['debit'] / st_line_currency_rate, company_currency)
                        aml_dict['credit'] = statement_currency.with_context(ctx).compute(aml_dict['credit'] / st_line_currency_rate, company_currency)
                    else:
                        # Statement is in foreign currency and no extra currency is given for the transaction
                        aml_dict['debit'] = st_line_currency.with_context(ctx).compute(aml_dict['debit'], company_currency)
                        aml_dict['credit'] = st_line_currency.with_context(ctx).compute(aml_dict['credit'], company_currency)
                elif statement_currency.id != company_currency.id:
                    # Statement is in foreign currency but the transaction is in company currency
                    prorata_factor = (aml_dict['debit'] - aml_dict['credit']) / self.amount_currency
                    aml_dict['amount_currency'] = prorata_factor * self.amount
                    aml_dict['currency_id'] = statement_currency.id

            # Create write-offs
            # When we register a payment on an invoice, the write-off line contains the amount
            # currency if all related invoices have the same currency. We apply the same logic in
            # the manual reconciliation.
            counterpart_aml = self.env['account.move.line']
            for aml_dict in counterpart_aml_dicts:
                counterpart_aml |= aml_dict.get('move_line', self.env['account.move.line'])
            new_aml_currency = False
            if counterpart_aml\
                    and len(counterpart_aml.mapped('currency_id')) == 1\
                    and counterpart_aml[0].currency_id\
                    and counterpart_aml[0].currency_id != company_currency:
                new_aml_currency = counterpart_aml[0].currency_id
            for aml_dict in new_aml_dicts:
                aml_dict['payment_id'] = payment and payment.id or False
                if new_aml_currency and not aml_dict.get('currency_id'):
                    aml_dict['currency_id'] = new_aml_currency.id
                    aml_dict['amount_currency'] = company_currency.with_context(ctx).compute(aml_dict['debit'] - aml_dict['credit'], new_aml_currency)
                aml_obj.with_context(check_move_validity=False, apply_taxes=True).create(aml_dict)

            # Create counterpart move lines and reconcile them
            for aml_dict in counterpart_aml_dicts:
                if aml_dict['move_line'].partner_id.id:
                    aml_dict['partner_id'] = aml_dict['move_line'].partner_id.id
                aml_dict['account_id'] = aml_dict['move_line'].account_id.id
                aml_dict['payment_id'] = payment and payment.id or False

                counterpart_move_line = aml_dict.pop('move_line')
                if counterpart_move_line.currency_id and counterpart_move_line.currency_id != company_currency and not aml_dict.get('currency_id'):
                    aml_dict['currency_id'] = counterpart_move_line.currency_id.id
                    aml_dict['amount_currency'] = company_currency.with_context(ctx).compute(aml_dict['debit'] - aml_dict['credit'], counterpart_move_line.currency_id)
                new_aml = aml_obj.with_context(check_move_validity=False).create(aml_dict)

                (new_aml | counterpart_move_line).reconcile()

            # Balance the move
            st_line_amount = -sum([x.balance for x in move.line_ids])
            aml_dict = self._prepare_reconciliation_move_line(move, st_line_amount)
            aml_dict['payment_id'] = payment and payment.id or False
            aml_obj.with_context(check_move_validity=False).create(aml_dict)

            move.post()
            #record the move name on the statement line to be able to retrieve it in case of unreconciliation
            self.write({'move_name': move.name})
            payment and payment.write({'payment_reference': move.name})
        elif self.move_name:
            raise UserError(_('Operation not allowed. Since your statement line already received a number, you cannot reconcile it entirely with existing journal entries otherwise it would make a gap in the numbering. You should book an entry and make a regular revert of it in case you want to cancel it.'))
        counterpart_moves.assert_balanced()
        return counterpart_moves
