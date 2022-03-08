# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sayooj A O(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_count = fields.Integer(string='Invoices', compute='_compute_invoice_count')
    operation_code = fields.Selection(related='picking_type_id.code')
    is_return = fields.Boolean()

    invoice_id  =  fields.Many2one('account.move', 'Factura Relacionada')

    invoice_refund_id  =  fields.Many2one('account.move', 'Nota de Credito Relacionada')


    def _compute_invoice_count(self):
        """This compute function used to count the number of invoice for the picking"""
        for picking_id in self:
            move_ids = picking_id.env['account.move'].search([('invoice_origin', '=', picking_id.name)])
            if move_ids:
                self.invoice_count = len(move_ids)
            else:
                self.invoice_count = 0

    def crear_factura_o_nc_desde_picking(self):
        
        if self.operation_code=='incoming': #Recepcion de Proveedor o Devolucion de Cliente
            # Recepcion de Proveedor
            if self.location_id.usage=='supplier' and self.location_dest_id.usage=='internal':
                invoice = self.create_bill()
            # Devolucion de Cliente    
            elif self.is_return or (self.location_id.usage=='customer' and self.location_dest_id.usage=='internal'): 
                _logger.info("self: %s" % self)
                invoice = self.create_customer_credit()
        elif self.operation_code=='outgoing': #Recepcion de Proveedor o Devolucion de Cliente
            # Entrega a Clientes
            if self.location_id.usage=='internal' and self.location_dest_id.usage=='customer':
                invoice = self.create_invoice()
            # Devolucion a Proveedor
            elif self.is_return or (self.location_id.usage=='internal' and self.location_dest_id.usage=='supplier'): 
                invoice = self.create_vendor_credit()
        return invoice
                
        
    
    def create_invoice(self):
        """This is the function for creating customer invoice
        from the picking"""
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = self.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("No se encontraron los diarios para la creación de facturas, revisa los ajustes de Contabilidad."))
                so = picking_id.move_ids_without_package[0].sale_line_id.order_id
                
                invoice_line_list = []
                fiscal_position_id  =  False
                partner_shipping_id = False
                analytic_account_id = False
                invoice_payment_term_id = False 
                partner_bank_id = False
                for move_ids_without_package in picking_id.move_ids_without_package:
                    sale_line_id = False
                    analytic_tag_ids = []
                    price_unit = 0.0
                    product_uom_id = False
                    taxes_ids  = []
                    if move_ids_without_package.sale_line_id:
                        price_unit = move_ids_without_package.sale_line_id.price_unit
                        product_uom_id = move_ids_without_package.sale_line_id.product_uom.id
                        order = move_ids_without_package.sale_line_id.order_id
                        sale_line_id = move_ids_without_package.sale_line_id.id 
                        if not fiscal_position_id:
                            fiscal_position_id  = (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(order.partner_id.id)).id
                        if not partner_shipping_id:
                            partner_shipping_id = order.partner_shipping_id.id
                        if not invoice_payment_term_id:
                            invoice_payment_term_id = order.payment_term_id.id
                        if not partner_bank_id:
                            partner_bank_id = order.company_id.partner_id.bank_ids[:1].id
                        if not analytic_account_id and order.analytic_account_id:
                            analytic_account_id = order.analytic_account_id.id
                        if move_ids_without_package.sale_line_id.analytic_tag_ids:
                            analytic_tag_ids =  move_ids_without_package.sale_line_id.analytic_tag_ids.ids
                        taxes_ids  = move_ids_without_package.sale_line_id.tax_id.ids if move_ids_without_package.sale_line_id.tax_id else False
                    else:
                        price_unit = move_ids_without_package.product_id.lst_price
                        product_uom_id = move_ids_without_package.product_uom.id

                    if move_ids_without_package.move_line_ids:
                        for smvline in move_ids_without_package.move_line_ids:
                            stock_prod_lot_ids = [smvline.lot_id.id] if smvline.lot_id else False
                            vals = (0, 0, {
                                'name': move_ids_without_package.description_picking,
                                'product_id': smvline.product_id.id,
                                'product_uom_id': smvline.product_uom_id.id,
                                'price_unit': price_unit,
                                'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                                else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                                'tax_ids': [(6, 0, taxes_ids)] if taxes_ids else False,
                                'quantity': smvline.qty_done,
                                'sale_line_ids': [(6, 0, [sale_line_id])] if sale_line_id else False,
                                'analytic_tag_ids': [(6, 0, analytic_tag_ids)] if analytic_tag_ids else False,
                                'analytic_account_id': analytic_account_id,
                                'stock_prod_lot_ids': stock_prod_lot_ids,
                                'sale_line_origin_id': sale_line_id,
                            })
                            invoice_line_list.append(vals)
                            if smvline.lot_id:
                                vals = (0, 0, {
                                    'name': smvline.lot_id.name,
                                    'display_type': 'line_note',
                                    'sale_line_origin_id': sale_line_id,
                                })
                                invoice_line_list.append(vals)
                    else:
                        vals = (0, 0, {
                            'name': move_ids_without_package.description_picking,
                            'product_id': move_ids_without_package.product_id.id,
                            'product_uom_id': move_ids_without_package.product_uom.id,
                            'price_unit': price_unit,
                            'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                            else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, taxes_ids)] if taxes_ids else False,
                            'quantity': move_ids_without_package.quantity_done,
                            'sale_line_ids': [(6, 0, [sale_line_id])] if sale_line_id else False,
                            'analytic_tag_ids': [(6, 0, analytic_tag_ids)] if analytic_tag_ids else False,
                            'product_uom_id': product_uom_id,
                            'analytic_account_id': analytic_account_id,
                        })
                        invoice_line_list.append(vals)
                invoice = picking_id.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': so.note or '',#picking_id.name + ('\n%s' % so.note),
                    'partner_id': so.partner_invoice_id.id or so.partner_id.id,
                    'currency_id': so.pricelist_id.currency_id.id or picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'payment_reference': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'fiscal_position_id': fiscal_position_id,
                    'partner_shipping_id': partner_shipping_id,
                    'invoice_payment_term_id': invoice_payment_term_id,
                    'partner_bank_id': partner_bank_id,
                    'ref'   : so.client_order_ref,
                })
                picking_id.invoice_id = invoice.id
                return invoice

    def create_bill(self):
        """This is the function for creating vendor bill
                from the picking"""
        for picking_id in self:
            current_user = self.env.uid
            po = picking_id.move_ids_without_package[0].purchase_line_id.order_id
            if picking_id.picking_type_id.code == 'incoming':
                vendor_journal_id = self.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.vendor_journal_id') or False
                if not vendor_journal_id:
                    raise UserError(_("No se encontraron los diarios para la creación de facturas, revisa los ajustes de Contabilidad."))
                invoice_line_list = []
                fiscal_position_id = False
                invoice_payment_term_id = False
                for move_ids_without_package in picking_id.move_ids_without_package:
                    taxes_ids = []
                    if move_ids_without_package.purchase_line_id:
                        taxes_ids = move_ids_without_package.purchase_line_id.taxes_id.ids if move_ids_without_package.purchase_line_id.taxes_id else False
                    else:
                        if move_ids_without_package.product_id.supplier_taxes_id:
                            taxes_ids = move_ids_without_package.product_id.supplier_taxes_id.ids
                    
                    price_unit = move_ids_without_package.purchase_line_id.price_unit or move_ids_without_package.product_id.standard_price
                    if move_ids_without_package.purchase_line_id:
                        price_unit  = move_ids_without_package.purchase_line_id.price_unit
                        order = move_ids_without_package.purchase_line_id.order_id
                        if not fiscal_position_id and order.fiscal_position_id:
                            fiscal_position_id = order.fiscal_position_id.id
                        if not invoice_payment_term_id and order.payment_term_id:
                            invoice_payment_term_id = order.payment_term_id.id 
                    analytic_account_id = False
                    purchase_line_id = False
                    if move_ids_without_package.purchase_line_id:
                        purchase_line_id  = move_ids_without_package.purchase_line_id
                        analytic_account_id = move_ids_without_package.purchase_line_id.id if move_ids_without_package.purchase_line_id else False

                        fiscal_position = move_ids_without_package.purchase_line_id.order_id.fiscal_position_id
                        accounts = move_ids_without_package.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
                        account_id =  accounts['expense'] or self.account_id
                        # if move_ids_without_package.is_sale_document(include_receipts=True):
                        #     # Out invoice.
                        #     account_id =  accounts['income']
                        # elif move_ids_without_package.is_purchase_document(include_receipts=True):
                        #     # In invoice.
                        #     account_id =  accounts['expense'] or self.account_id

                    else:
                        account_id = move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id \
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id

                    vals = (0, 0, {
                        'name': move_ids_without_package.description_picking,
                        'product_id': move_ids_without_package.product_id.id,
                        'product_uom_id': move_ids_without_package.product_uom.id,
                        'price_unit': price_unit,
                        'account_id': account_id,
                        'tax_ids': [(6, 0, taxes_ids)] if taxes_ids else False,
                        # 'analytic_account_id': analytic_account_id,
                        'purchase_line_id': purchase_line_id,
                        'quantity': move_ids_without_package.quantity_done,
                    })
                    invoice_line_list.append(vals)
                purchase_id = False
                if picking_id.purchase_id:
                    purchase_id = picking_id.purchase_id.id

                invoice = picking_id.env['account.move'].create({
                    'move_type': 'in_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.commercial_partner_id.id,
                    'currency_id': po.currency_id.id or picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(vendor_journal_id),
                    'payment_reference': picking_id.name,
                    'picking_id': picking_id.id,
                    'purchase_id': purchase_id,
                    'invoice_line_ids': invoice_line_list,
                    'fiscal_position_id': fiscal_position_id,
                    'invoice_payment_term_id': invoice_payment_term_id,
                })
                picking_id.invoice_id = invoice.id
                return invoice

    def create_customer_credit(self):
        """This is the function for creating customer credit note
                from the picking"""
        for picking_id in self:
            current_user = picking_id.env.uid
            so = picking_id.move_ids_without_package[0].sale_line_id.order_id
            if picking_id.picking_type_id.code == 'incoming':
                customer_journal_id = self.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("No se encontraron los diarios para la creación de facturas, revisa los ajustes de Contabilidad."))
                invoice_line_list = []

                for move_ids_without_package in picking_id.move_ids_without_package:
                    if move_ids_without_package.move_line_ids:
                        for smvline in move_ids_without_package.move_line_ids:
                            dev_prod_lot_ids = [smvline.lot_id.id] if smvline.lot_id else False
                            vals = (0, 0, {
                                'name': move_ids_without_package.description_picking,
                                'product_id': smvline.product_id.id,
                                'product_uom_id': smvline.product_uom_id.id,
                                'price_unit': move_ids_without_package.sale_line_id.price_unit or move_ids_without_package.product_id.lst_price,
                                'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                                else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                                'tax_ids': [(6, 0, picking_id.company_id.account_sale_tax_id and [picking_id.company_id.account_sale_tax_id.id] or [])],
                                'quantity': smvline.qty_done,
                                'dev_prod_lot_ids': [(6, 0, dev_prod_lot_ids)] if dev_prod_lot_ids else False,
                            })
                            invoice_line_list.append(vals)
                            if smvline.lot_id:
                                vals = (0, 0, {
                                    'name': smvline.lot_id.name,
                                    'display_type': 'line_note',
                                })
                                invoice_line_list.append(vals)
                    else:
                            vals = (0, 0, {
                                'name': move_ids_without_package.description_picking,
                                'product_id': move_ids_without_package.product_id.id,
                                'product_uom_id': move_ids_without_package.product_uom.id,
                                'price_unit': move_ids_without_package.sale_line_id.price_unit or move_ids_without_package.product_id.lst_price,
                                'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                                else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                                'tax_ids': [(6, 0, picking_id.company_id.account_sale_tax_id and [picking_id.company_id.account_sale_tax_id.id] or [])],
                                'quantity': move_ids_without_package.quantity_done,
                            })
                            invoice_line_list.append(vals)

                # for move_ids_without_package in picking_id.move_ids_without_package:
                #     vals = (0, 0, {
                #         'name': move_ids_without_package.description_picking,
                #         'product_id': move_ids_without_package.product_id.id,
                #         'product_uom_id': move_ids_without_package.product_uom.id,
                #         'price_unit': move_ids_without_package.sale_line_id.price_unit or move_ids_without_package.product_id.lst_price,
                #         'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                #         else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                #         'tax_ids': [(6, 0, picking_id.company_id.account_sale_tax_id and [picking_id.company_id.account_sale_tax_id.id] or [])],
                #         'quantity': move_ids_without_package.quantity_done,
                #     })
                #     invoice_line_list.append(vals)
                invoice = picking_id.env['account.move'].create({
                        'move_type': 'out_refund',
                        'invoice_origin': picking_id.name,
                        'invoice_user_id': current_user,
                        'narration': picking_id.note,# picking_id.name + '\n' + picking_id.note,
                        'partner_id': so.partner_id.commercial_partner_id.id or picking_id.partner_id.id,
                        'partner_shipping_id': so.partner_id.commercial_partner_id.id or picking_id.partner_id.id,
                        #'partner_id': so.partner_invoice_id.id or so.partner_id.id,
                        'currency_id': so.pricelist_id.currency_id.id or picking_id.env.user.company_id.currency_id.id,
                        'journal_id': int(customer_journal_id),
                        'payment_reference': picking_id.name,
                        'picking_id': picking_id.id,
                        'invoice_line_ids': invoice_line_list
                    })
                picking_id.invoice_refund_id = invoice.id
                return invoice

    def create_vendor_credit(self):
        """This is the function for creating refund
                from the picking"""
        for picking_id in self:
            current_user = self.env.uid
            po = picking_id.move_ids_without_package[0].purchase_line_id.order_id
            if picking_id.picking_type_id.code == 'outgoing':
                vendor_journal_id = self.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.vendor_journal_id') or False
                if not vendor_journal_id:
                    raise UserError(_("No se encontraron los diarios para la creación de facturas, revisa los ajustes de Contabilidad."))
                invoice_line_list = []
                for move_ids_without_package in picking_id.move_ids_without_package:
                    vals = (0, 0, {
                        'name': move_ids_without_package.description_picking,
                        'product_id': move_ids_without_package.product_id.id,
                        'product_uom_id': move_ids_without_package.product_uom.id,
                        'price_unit': move_ids_without_package.purchase_line_id.price_unit or move_ids_without_package.product_id.lst_price,
                        'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                        'tax_ids': [(6, 0, picking_id.company_id.account_purchase_tax_id and [picking_id.company_id.account_purchase_tax_id.id] or [])],
                        'quantity': move_ids_without_package.quantity_done,
                    })
                    invoice_line_list.append(vals)
                invoice = picking_id.env['account.move'].create({
                        'move_type': 'in_refund',
                        'invoice_origin': picking_id.name,
                        'invoice_user_id': current_user,
                        'narration': picking_id.name,
                        'partner_id': picking_id.partner_id.commercial_partner_id.id,
                        'currency_id': po.currency_id.id or picking_id.env.user.company_id.currency_id.id,
                        'journal_id': int(vendor_journal_id),
                        'payment_reference': picking_id.name,
                        'picking_id': picking_id.id,
                        'invoice_line_ids': invoice_line_list
                    })
                picking_id.invoice_refund_id = invoice.id
                return invoice

    def action_open_picking_invoice(self):
        """This is the function of the smart button which redirect to the
        invoice related to the current picking"""
        return {
            'name': 'Facturas',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.name)],
            'context': {'create': False},
            'target': 'current'
        }


class StockReturnInvoicePicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        """in this function the picking is marked as return"""
        new_picking, pick_type_id = super(StockReturnInvoicePicking, self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        picking.write({'is_return': True})
        return new_picking, pick_type_id
