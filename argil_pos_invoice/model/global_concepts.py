# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

class Company(models.Model):
    _inherit = 'res.company'

    product_for_global_invoice = fields.Many2one("product.product", "Producto Facturas Globales",
                                  help="Producto para Generar el Descuento Global")
    invoice_public_default = fields.Boolean('Marcar Publico General', 
        help='Indica si el Asistente de Factura Global marcara el campo de Factura a Publico en General por defecto.', )


class SaleOrderLineGlobalConcept(models.Model):
    _name = 'sale.order.line.global.concept'
    _description = 'Concetps de Facturación Global'
    _rec_name = 'noidentificacion' 

    noidentificacion = fields.Char('NoIdentificacion', size=128)
    product_id = fields.Many2one('product.product', 'Producto')
    uom_id = fields.Many2one('uom.uom', 'Unidad de Medida')
    invoice_line_tax_ids = fields.Many2many('account.tax',
        'sale_order_account_invoice_line_global_tax', 'global_line_id', 'tax_id',
        string='Impuestos',)
    quantity = fields.Float('Cantidad', digits=(14,2), default=1.0)
    price_unit = fields.Float('Total')
    sale_id = fields.Many2one('sale.order', 'ID Ref')

class PosOrderLineGlobalConcept(models.Model):
    _name = 'pos.order.line.global.concept'
    _description = 'Concetps de Facturación Global'
    _rec_name = 'noidentificacion' 

    noidentificacion = fields.Char('NoIdentificacion', size=128)
    product_id = fields.Many2one('product.product', 'Producto')
    uom_id = fields.Many2one('uom.uom', 'Unidad de Medida')
    invoice_line_tax_ids = fields.Many2many('account.tax',
        'pos_order_account_invoice_line_global_tax', 'global_line_id', 'tax_id',
        string='Impuestos',)
    quantity = fields.Float('Cantidad', digits=(14,2), default=1.0)
    price_unit = fields.Float('Total')
    sale_id = fields.Many2one('pos.order', 'ID Ref')

class Company(models.Model):
    _inherit = 'res.company'

    product_for_global_invoice = fields.Many2one("product.product", "Producto Facturas Globales",
                                  help="Producto para Generar el Descuento Global")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_for_global_invoice = fields.Many2one("product.product", "Producto Facturas Globales",
                                  related='company_id.product_for_global_invoice',
                                  help="Producto para Generar el Descuento Global")

    # @api.onchange('company_id')
    # def onchange_company_id(self):
    #     if self.company_id:
    #         company = self.company_id
    #         self.product_for_global_invoice = company.product_for_global_invoice.id
    #         res = super(ResConfigSettings, self).onchange_company_id()
    #         return res

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit ='sale.order'


    @api.depends('state', 'order_line.invoice_status','invoice_ids')
    def _get_invoiced(self):

        """
        Compute the invoice status of a SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also hte default value if the conditions of no other status is met.
        - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
        - invoiced: if all SO lines are invoiced, the SO is invoiced.
        - upselling: if all SO lines are invoiced or upselling, the status is upselling.

        The invoice_ids are obtained thanks to the invoice lines of the SO lines, and we also search
        for possible refunds created directly from existing invoices. This is necessary since such a
        refund is not directly linked to the SO.
        """
        for order in self:
            if order.invoice_global_ids:
                invoice_ids = [x.id for x in order.invoice_global_ids]
                invoice_ids = self.env['account.move'].browse(invoice_ids)
            else:
                invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id')
                # Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
                # 'account.invoice.refund')
                # use like as origin may contains multiple references (e.g. 'SO01, SO02')
                refunds = invoice_ids.search([('origin', 'like', order.name)])
                invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])
                # Search for refunds as well
            refund_ids = self.env['account.move'].browse()
            if invoice_ids:
                for inv in invoice_ids:
                    refund_ids += refund_ids.search([('move_type', '=', 'out_refund'), ('origin', '=', inv.number), ('origin', '!=', False), ('journal_id', '=', inv.journal_id.id)])

            line_invoice_status = [line.invoice_status for line in order.order_line]

            if order.state not in ('sale', 'done'):
                invoice_status = 'no'
            elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                invoice_status = 'to invoice'
            elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                invoice_status = 'invoiced'
            elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
                invoice_status = 'upselling'
            else:
                invoice_status = 'no'

            order.update({
                'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
                'invoice_ids': invoice_ids.ids + refund_ids.ids,
                'invoice_status': invoice_status
            })

    global_line_ids = fields.One2many('sale.order.line.global.concept', 'sale_id', 'Conceptos de Facturacion Global')
    invoice_global_ids = fields.Many2many('account.move',
        'account_invoice_sale_rel', 'sale_id', 'invoice_id',
        string='Facturas', copy=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            rec.update_concepts_to_global_invoice()
        return res

    def search_product_global(self):
        for rec in self:
            product_uom = self.env['uom.uom']
            product_obj = self.env['product.product']
            company = rec.company_id
            if not company.product_for_global_invoice:
                uom_id = product_uom.search([('name','=','Actividad Facturacion')])
                uom_id = uom_id[0] if uom_id else False
                if not uom_id:
                    sat_udm  = self.env['sat.udm']
                    sat_uom_id = sat_udm.search([('code','=','ACT')])
                    if not sat_uom_id:
                        raise UserError("Error!\nNo existe la Unidad de Medida ACT.")
                    uom_id = product_uom.create({'sat_uom_id':sat_uom_id[0].id,
                                                 'name':'Actividad Facturacion',
                                                 'category_id': 1})
                sat_product_id = self.env['sat.producto'].search([('code','=','01010101')])
                if not sat_product_id:
                    raise UserError("El Codigo 01010101 no existe en el Catalogo del SAT.")
                product_id = product_obj.search([('product_for_global_invoice','=',True)])
                if product_id:
                    product_id = product_id[0]
                else:
                    product_id = product_obj.create({
                            'name': 'Servicio Facturacion Global',
                            'uom_id': uom_id.id,
                            'uom_po_id': uom_id.id,
                            'type': 'service',
                            'sat_product_id': sat_product_id[0].id,
                            'product_for_global_invoice': True,
                        })
                company.write({'product_for_global_invoice': product_id.id})
            else:
                product_id = company.product_for_global_invoice

            return product_id

    def update_concepts_to_global_invoice(self):
        inv_ref = self.env['account.move']
        acc_tax_obj = self.env['account.tax']
        inv_line_ref = self.env['account.move.line']
        product_obj = self.env['product.product']
        sales_order_obj = self.env['sale.order']
        order_line_obj = self.env['sale.order.line']
        picking_obj = self.env['stock.picking']

        for rec in self:
            if rec.global_line_ids:
                rec.global_line_ids.unlink()
            inv_ids = []
            lines = {}
            for line in rec.order_line:
                ## Agrupamos las líneas según el impuesto
                xval = 0.0
                taxes_list = [x.id for x in line.product_id.taxes_id]
                for tax in acc_tax_obj.browse(taxes_list):
                    xval += (tax.price_include and tax.amount or 0.0)

                tax_names = ", ".join([x.name for x in line.product_id.taxes_id])
                val={
                    'tax_names'           : ", ".join([x.name for x in line.product_id.taxes_id]),
                    'taxes_id'            : ",".join([str(x.id) for x in line.product_id.taxes_id]),
                    'price_subtotal'      : line.price_subtotal * (1.0 + xval),
                    'price_subtotal_incl' : line.price_subtotal,
                    }
                key = (val['tax_names'],val['taxes_id'])
                if not key in lines:
                    lines[key] = val
                    lines[key]['price_subtotal'] = val['price_subtotal']
                    lines[key]['price_subtotal_incl'] = val['price_subtotal_incl']

                else:
                    lines[key]['price_subtotal'] += val['price_subtotal']

            global_line_ids = []
            product_global = rec.search_product_global()
            for key, line in lines.items():
                tax_name = ''
                taxes_ids = line['taxes_id'].split(',') if line['taxes_id'] else False
                if taxes_ids:
                    taxes_ids = [int(x) for x in taxes_ids]
                global_vals = {
                    'product_id': product_global.id,
                    'noidentificacion': rec.name,
                    'uom_id': product_global.uom_id.id,
                    'invoice_line_tax_ids': [(6, 0, taxes_ids)] if line['taxes_id'] else False,
                    'quantity': 1,
                    'price_unit': line['price_subtotal'],
                }
                global_line_ids.append((0,0, global_vals))
            if global_line_ids:
                rec.write({'global_line_ids': global_line_ids})

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit ='product.product'

    product_for_global_invoice = fields.Boolean('Facturacion Global')

### TPV ####
class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit ='pos.order'

    global_line_ids = fields.One2many('pos.order.line.global.concept', 'sale_id', 'Conceptos de Facturacion Global')

    def add_payment(self, data):
        res = super(PosOrder, self).add_payment(data)

        for rec in self:
            rec.update_concepts_to_global_invoice()
        return res

    def search_product_global(self):
        for rec in self:
            product_uom = self.env['uom.uom']
            product_obj = self.env['product.product']
            uom_category = self.env['uom.category'].sudo()
            company = rec.company_id
            if not company.product_for_global_invoice:
                uom_id = product_uom.search([('name','=','Actividad Facturacion')])
                uom_id = uom_id[0] if uom_id else False
                if not uom_id:
                    sat_udm  = self.env['sat.udm']
                    sat_uom_id = sat_udm.search([('code','=','ACT')])
                    if not sat_uom_id:
                        raise UserError("Error!\nNo existe la Unidad de Medida ACT.")
                    category_fact = uom_category.create({'name':'Facturacion Electronica'})
                    uom_id = product_uom.create({'sat_uom_id':sat_uom_id.id,
                                                 'name':'Actividad Facturacion',
                                                 'uom_type': 'reference',
                                                 'category_id': category_fact.id,
                                                 'use_4_invoice_general_public': True,
                                                 })
                sat_product_id = self.env['sat.producto'].search([('code','=','01010101')])
                if not sat_product_id:
                    raise UserError("El Codigo 01010101 no existe en el Catalogo del SAT.")
                product_id = product_obj.search([('product_for_global_invoice','=',True)])
                if product_id:
                    product_id = product_id[0]
                else:
                    product_id = product_obj.create({
                            'name': 'Servicio Facturacion Global',
                            'uom_id': uom_id.id,
                            'uom_po_id': uom_id.id,
                            'type': 'service',
                            'sat_product_id': sat_product_id[0].id,
                            'product_for_global_invoice': True,
                        })
                company.write({'product_for_global_invoice': product_id.id})
            else:
                product_id = company.product_for_global_invoice

            return product_id

    def update_concepts_to_global_invoice(self):
        inv_ref = self.env['account.move']
        acc_tax_obj = self.env['account.tax']
        inv_line_ref = self.env['account.move.line']
        product_obj = self.env['product.product']
        picking_obj = self.env['stock.picking']

        for rec in self:
            if rec.global_line_ids:
                rec.global_line_ids.unlink()
            inv_ids = []
            lines = {}
            for line in rec.lines:
                ## Agrupamos las líneas según el impuesto
                xval = 0.0
                taxes_list = [x.id for x in line.product_id.taxes_id]
                for tax in acc_tax_obj.browse(taxes_list):
                    xval += (tax.price_include and tax.amount or 0.0)

                tax_names = ", ".join([x.name for x in line.product_id.taxes_id])
                val={
                    'tax_names'           : ", ".join([x.name for x in line.product_id.taxes_id]),
                    'taxes_id'            : ",".join([str(x.id) for x in line.product_id.taxes_id]),
                    'price_subtotal'      : line.price_subtotal * (1.0 + xval),
                    'price_subtotal_incl' : line.price_subtotal,
                    }
                key = (val['tax_names'],val['taxes_id'])
                if not key in lines:
                    lines[key] = val
                    lines[key]['price_subtotal'] = val['price_subtotal']
                    lines[key]['price_subtotal_incl'] = val['price_subtotal_incl']

                else:
                    lines[key]['price_subtotal'] += val['price_subtotal']

            global_line_ids = []
            product_global = rec.search_product_global()
            for key, line in lines.items():
                tax_name = ''
                taxes_ids = line['taxes_id'].split(',') if line['taxes_id'] else False
                if taxes_ids:
                    taxes_ids = [int(x) for x in taxes_ids]
                global_vals = {
                    'product_id': product_global.id,
                    'noidentificacion': rec.name,
                    'uom_id': product_global.uom_id.id,
                    'invoice_line_tax_ids': [(6, 0, taxes_ids)] if line['taxes_id'] else False,
                    'quantity': 1,
                    'price_unit': line['price_subtotal'],
                }
                global_line_ids.append((0,0, global_vals))
            if global_line_ids:
                rec.write({'global_line_ids': global_line_ids})


class AccountInvoiceLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'

    noidentificacion = fields.Char('NoIdentificacion', size=128)

    def update_properties_concept(self, concepto):
        res = super(AccountInvoiceLine, self).update_properties_concept(concepto)
        for rec in self:
            if rec.noidentificacion:
                res.update({'NoIdentificacion':rec.noidentificacion})
        return res
