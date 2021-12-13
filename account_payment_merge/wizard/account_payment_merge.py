# -*- encoding: utf-8 -*-   

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    merged = fields.Boolean('Fusionado')


    def group_moves_data_in_payment(self, main_payment, main_move):
        account_move_lines_groupped_credit = []
        account_move_lines_groupped_debit = []
        finally_amount_groupped_credit = 0.0
        finally_amount_groupped_debit = 0.0
        finally_amount_currency_credit = 0.0
        finally_amount_currency_debit = 0.0
        destination_account_id = main_payment.destination_account_id.id
        destination_journal_id = main_payment.journal_id.id
        account_journal_id = main_payment.payment_type in ('outbound','transfer') and main_payment.journal_id.payment_credit_account_id.id or main_payment.journal_id.payment_credit_account_id.id
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
            if payment.cfdi_folio_fiscal:
                raise ValidationError(_("Advertencia !!!\nNo puede fusionar Pagos si ya se encuentran con Timbre Fiscal (Pago: %s)") % payment.name)
            if payment.state != 'posted':
                raise ValidationError(_("Advertencia !!!\nNo puede fusionar Pagos si NO se encuentran Confirmados (Pago: %s)") % payment.name)
            
        return res

    def merge_payments(self):
        account_payment_invoice_obj = self.env['account.payment.invoice']
        main_payment = self.payment_ids[0]
        main_move = main_payment.move_id
        payment_reference = main_payment.payment_reference
        amount = main_payment.amount
        factoraje = 'monto_factoraje_financiero' in main_payment._fields and main_payment.monto_factoraje_financiero or 0.0
        _logger.info("factoraje: %s" % factoraje)
        for payment in self.payment_ids:
            if main_payment == payment:
                continue
            _logger.info("Procesando el pago: %s" % payment.name)
            amount += payment.amount
            factoraje += 'monto_factoraje_financiero' in payment._fields and payment.monto_factoraje_financiero or 0.0
            if 'monto_factoraje_financiero' in main_payment._fields:
                _logger.info("payment.monto_factoraje_financiero: %s" % payment.monto_factoraje_financiero)
            else:
                _logger.info("El registro %s no contiene Factoraje Financiero (payment.monto_factoraje_financiero)" % payment.name)
            move = payment.move_id

            account_payment_invoice_ids = payment.payment_invoice_line_ids
            payment_move_line_ids = payment.move_id.line_ids.ids
            _logger.info("\n:::: payment_move_line_ids %s >>>>>>>>> " % payment_move_line_ids)
            
            query = """
            update account_move_line set move_id=%s, payment_id=%s where id in %s;
            delete from account_move where id=%s;
            """ % (main_move.id, main_payment.id, tuple(payment.move_id.line_ids.ids), move.id)
            #_logger.info("query: %s" % query)
            self._cr.execute(query)
            payment.state = 'cancel'
            payment.payment_invoice_line_ids.write({'payment_id': main_payment.id})
            if payment.payment_reference:
                if payment_reference:
                    payment_reference += ' : ' + payment.payment_reference
                else:
                    payment_reference = payment.payment_reference
        ### Recorriendo los Pagos  - Agrupando la cuenta de Bancos###
        self.payment_ids.group_moves_data_in_payment(main_payment,main_move)

        xdata = {'amount' : amount, 'payment_reference' : payment_reference, 'merged': True}
        _logger.info("factoraje: %s" % factoraje)
        if 'monto_factoraje_financiero' in main_payment._fields and factoraje:
            xdata['monto_factoraje_financiero'] = factoraje
        _logger.info("xdata: %s" % xdata)
        main_payment.write(xdata)
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




    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
