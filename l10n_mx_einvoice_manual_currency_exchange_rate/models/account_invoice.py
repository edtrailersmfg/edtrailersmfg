# -*- coding: utf-8 -*-

from odoo import fields, models,api,_
from odoo.exceptions import UserError
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class account_invoice_line(models.Model):
    _inherit ='account.move.line'
    

    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        ''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
        in some business fields (affecting the 'price_subtotal' field).

        :param price_subtotal:  The untaxed amount.
        :param move_type:       The type of the move.
        :param currency:        The line's currency.
        :param company:         The move's company.
        :param date:            The move's date.
        :return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1

        amount_currency = price_subtotal * sign

        if self.move_id.manual_currency_rate_active:
            if self.move_id.manual_currency_rate > 0:
                currency_rate = self.company_id.currency_id.rate / self.move_id.manual_currency_rate
                balance = amount_currency*currency_rate
            else:
                balance = currency._convert(amount_currency, company.currency_id, company,
                                            date or fields.Date.context_today(self))

        else:
            balance = currency._convert(amount_currency, company.currency_id, company,
                                        date or fields.Date.context_today(self))

        return {
            'amount_currency': amount_currency,
            'currency_id': currency.id,
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
        }


    @api.onchange('amount_currency')
    def _onchange_amount_currency(self):
        for line in self:
            company = line.move_id.company_id
            if line.move_id.manual_currency_rate > 0:
                currency_rate = line.company_id.currency_id.rate / line.move_id.manual_currency_rate
                balance = line.amount_currency*currency_rate
            else:
                balance = line.currency_id._convert(line.amount_currency, company.currency_id, company, line.move_id.date or fields.Date.context_today(line))
            line.debit = balance if balance > 0.0 else 0.0
            line.credit = -balance if balance < 0.0 else 0.0

            if not line.move_id.is_invoice(include_receipts=True):
                continue

            line.update(line._get_fields_onchange_balance())
            line.update(line._get_price_total_and_subtotal())


    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue

            line.name = line._get_computed_name()
            line.account_id = line._get_computed_account()
            taxes = line._get_computed_taxes()
            if taxes and line.move_id.fiscal_position_id:
                taxes = line.move_id.fiscal_position_id.map_tax(taxes)
            line.tax_ids = taxes
            line.product_uom_id = line._get_computed_uom()
            line.price_unit = line._get_computed_price_unit()

            # price_unit and taxes may need to be adapted following Fiscal Position
            line._set_price_and_tax_after_fpos()

            # # Convert the unit price to the invoice's currency.
            company = line.move_id.company_id
            
            if line.move_id.manual_currency_rate_active:
                currency_rate = line.move_id.manual_currency_rate/company.currency_id.rate
                if line.move_id.is_sale_document(include_receipts=True):
                    price_unit = line.product_id.lst_price
                elif line.move_id.is_purchase_document(include_receipts=True):
                    price_unit = line.product_id.standard_price
                else:
                    return 0.0
                manual_currency_rate = price_unit * currency_rate
                line.price_unit = manual_currency_rate



    @api.onchange('product_uom_id')
    def _onchange_uom_id(self):
        ''' Recompute the 'price_unit' depending of the unit of measure. '''
        if self.display_type in ('line_section', 'line_note'):
            return
        taxes = self._get_computed_taxes()
        if taxes and self.move_id.fiscal_position_id:
            taxes = self.move_id.fiscal_position_id.map_tax(taxes)
        self.tax_ids = taxes
        self.price_unit = self._get_computed_price_unit()
        company = self.move_id.company_id

        if self.move_id.manual_currency_rate_active:
            currency_rate = self.move_id.manual_currency_rate/company.currency_id.rate
            if self.move_id.is_sale_document(include_receipts=True):
                price_unit = self.product_id.lst_price
            elif self.move_id.is_purchase_document(include_receipts=True):
                price_unit = self.product_id.standard_price
            else:
                return 0.0
            manual_currency_rate = price_unit * currency_rate
            self.price_unit = manual_currency_rate
          
          
        
class account_invoice(models.Model):
    _inherit ='account.move'
    
    def _get_current_currency_rate(self):
        for rec in self:
            current_currency_rate = 1
            if rec.company_id.currency_id != rec.currency_id:
                currency = rec.currency_id
                date_ctx = {'date': rec.date_invoice_tz and rec.date_invoice_tz.date() or rec.invoice_date or fields.Date.context_today}
                currency_context = rec.currency_id.with_context(date_ctx)
                _logger.info("\n############### currency_context: %s" % currency_context)
                _logger.info("\n############### currency_context.rate: %s" % currency_context.rate)
                current_currency_rate = currency_context.rate
                if current_currency_rate == 1.0:
                    current_currency_rate = 1
                else:
                    current_currency_rate = 1.0 / current_currency_rate 
                _logger.info("\n############### current_currency_rate (compute): %s" % current_currency_rate)
            rec.current_currency_rate = current_currency_rate

    manual_currency_rate_active = fields.Boolean('Aplicar T.C. Manual', copy=False)
    manual_currency_rate = fields.Float('Rate', digits=(12, 6), copy=False)

    manual_currency_rate_invert = fields.Float('Tipo de Cambio', digits=(12, 6), copy=False)
    
    current_currency_rate = fields.Float('Tipo de Cambio', digits=(12, 6), compute="_get_current_currency_rate")

    ######################## Timbrado Electronico ##########################

    def _get_currency_exchange_rate_from_invoice_cce(self):
        rate = self.manual_currency_rate_invert
        if not rate:
            return super(account_invoice, self)._get_currency_exchange_rate_from_invoice_cce()
        return rate

    def _get_currency_exchange_rate_from_invoice(self, invoice, date_ctx):
        rate = invoice.manual_currency_rate_invert
        if not rate:
            return super(account_invoice, self)._get_currency_exchange_rate_from_invoice(invoice, date_ctx)
        return rate


    ######################## FIN - Timbrado Electronico ##########################

    @api.onchange('manual_currency_rate_invert')
    def onchange_manual_currency_rate_invert(self):
        if self.manual_currency_rate_invert:
            if self.manual_currency_rate_invert > 1.0:
                self.manual_currency_rate = 1.0 / self.manual_currency_rate_invert
            else:
                self.manual_currency_rate = self.manual_currency_rate_invert


    @api.constrains("manual_currency_rate")
    def _check_manual_currency_rate(self):
        for record in self:
            if record.manual_currency_rate_active:
                if record.manual_currency_rate == 0:
                    raise UserError(_('Exchange Rate Field is required , Please fill that.'))

    @api.onchange('manual_currency_rate_active', 'currency_id')
    def check_currency_id(self):
        if self.manual_currency_rate_active:
            if self.currency_id == self.company_id.currency_id:
                self.manual_currency_rate_active = False
                raise UserError(_('Company currency and invoice currency same, You can not added manual Exchange rate in same currency.'))

    def action_post(self):
        no_exchange_difference = False
        for rec in self:
            if rec.manual_currency_rate_active:
                no_exchange_difference = True
                for line in rec.invoice_line_ids:
                    prev_price = line.price_unit
                    line.price_unit = line.price_unit + 0.5
                    line.price_unit = prev_price
        ##### CHERMAN 2024 #####
        # Si tiene fecha de cambio modificada no genera movimiento de ajuste de tipos de cambio....
        if no_exchange_difference:
            res = super(account_invoice, self.with_context(no_exchange_difference=True)).action_post()   
        else:
            res = super(account_invoice, self).action_post()   
        ########################
        return res

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        """ Compute the dynamic tax lines of the journal entry.

        :param recompute_tax_base_amount: Flag forcing only the recomputation of the `tax_base_amount` field.
        """
        self.ensure_one()
        in_draft_mode = self != self._origin

        def _serialize_tax_grouping_key(grouping_dict):
            ''' Serialize the dictionary values to be used in the taxes_map.
            :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
            :return: A string representing the values.
            '''
            return '-'.join(str(v) for v in grouping_dict.values())

        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                is_refund = move.move_type in ('out_refund', 'in_refund')
                price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
            else:
                handle_price_include = False
                quantity = 1.0
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
                price_unit_wo_discount = base_line.amount_currency

            return base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_wo_discount,
                currency=base_line.currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
                include_caba_tags=move.always_tax_exigible,
            )

        taxes_map = {}

        # ==== Add tax lines ====
        to_remove = self.env['account.move.line']
        for line in self.line_ids.filtered('tax_repartition_line_id'):
            grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
            grouping_key = _serialize_tax_grouping_key(grouping_dict)
            if grouping_key in taxes_map:
                # A line with the same key does already exist, we only need one
                # to modify it; we have to drop this one.
                to_remove += line
            else:
                taxes_map[grouping_key] = {
                    'tax_line': line,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                }
        if not recompute_tax_base_amount:
            self.line_ids -= to_remove

        # ==== Mount base lines ====
        for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
            # Don't call compute_all if there is no tax.
            if not line.tax_ids:
                if not recompute_tax_base_amount:
                    line.tax_tag_ids = [(5, 0, 0)]
                continue

            compute_all_vals = _compute_base_line_taxes(line)

            # Assign tags on base line
            if not recompute_tax_base_amount:
                line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

            for tax_vals in compute_all_vals['taxes']:
                grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
                grouping_key = _serialize_tax_grouping_key(grouping_dict)

                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

                taxes_map_entry = taxes_map.setdefault(grouping_key, {
                    'tax_line': None,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                })
                taxes_map_entry['amount'] += tax_vals['amount']
                taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
                taxes_map_entry['grouping_dict'] = grouping_dict

        # ==== Pre-process taxes_map ====
        taxes_map = self._preprocess_taxes_map(taxes_map)

        # ==== Process taxes_map ====
        for taxes_map_entry in taxes_map.values():
            # The tax line is no longer used in any base lines, drop it.
            if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
                if not recompute_tax_base_amount:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

            # tax_base_amount field is expressed using the company currency.
            tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id, self.company_id, self.date or fields.Date.context_today(self))

            # Recompute only the tax_base_amount.
            if recompute_tax_base_amount:
                if taxes_map_entry['tax_line']:
                    taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
                continue
            if self.manual_currency_rate_active:
                if self.manual_currency_rate:
                    currency_rate = self.company_id.currency_id.rate/self.manual_currency_rate
                    balance = taxes_map_entry['amount'] * currency_rate
                else:
                    raise ValidationError(_("Please define Rate value."))
            else:
                balance = currency._convert(
                    taxes_map_entry['amount'],
                    self.company_currency_id,
                    self.company_id,
                    self.date or fields.Date.context_today(self),
                )
            to_write_on_line = {
                'amount_currency': taxes_map_entry['amount'],
                'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
                'tax_base_amount': tax_base_amount,
            }

            if taxes_map_entry['tax_line']:
                # Update an existing tax line.
                taxes_map_entry['tax_line'].update(to_write_on_line)
            else:
                # Create a new tax line.
                create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
                taxes_map_entry['tax_line'] = create_method({
                    **to_write_on_line,
                    'name': tax.name,
                    'move_id': self.id,
                    'company_id': self.company_id.id,
                    'company_currency_id': self.company_currency_id.id,
                    'tax_base_amount': tax_base_amount,
                    'exclude_from_invoice_tab': True,
                    **taxes_map_entry['grouping_dict'],
                })

            if in_draft_mode:
                taxes_map_entry['tax_line'].update(taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))


# # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
