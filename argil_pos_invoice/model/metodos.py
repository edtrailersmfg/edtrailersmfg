# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError


class account_move(models.Model):
    _inherit = 'account.move'

    def post(self):
        moves_to_post = [move for move in self if not move.journal_id.pos_dont_create_entries]
        moves_to_unlink = [move for move in self if move.journal_id.pos_dont_create_entries]
        res = True
        if moves_to_unlink:
            for mv in moves_to_unlink:
                mv.unlink()
            #moves_to_unlink.unlink()
        if moves_to_post:
            res = super(account_move, self).post()
        return res

    
class account_invoice_pos_reconcile_with_payments(models.TransientModel):
    _name = "account.invoice.pos_reconcile_with_payments"
    _description = "Wizard to Reconcile POS Payments with Invoices from POS Orders"

    date = fields.Date(string='Payment Date', help='This date will be used as the payment date !', 
                       default=fields.Date.context_today, required=True)
	
    
    def get_aml_to_reconcile(self, am_ids):
        am_obj = self.pool.get('account.move')
        amls = []
        for move in am_obj.browse(am_ids):
            for line in move.line_id:
                if line.account_id.type=='receivable':
                    #print "line: %s - %s - %s" % (move.name, line.account_id.code, line.account_id.name)
                    amls.append(line.id)
        return amls
	
    def reconcile_invoice_with_pos_payments(self):
        rec_ids = self._context.get('active_ids', [])
        
        am_obj = self.env['account.move']
        pos_order_obj = self.env['pos.order']
        
        for invoice in self.env['account.move'].browse(rec_ids):
            amls_to_reconcile = self.env['account.move.line']
            #print "----------------------------------------"
            #print "Procesando Factura: ", invoice.number
            if invoice.state != 'open':
                continue                
            order_ids = pos_order_obj.search([('account_move','=',invoice.id)])
            data_statement_line_ids, data_aml_ids = [], []
            for order in order_ids:
                #print "order: %s - %s " % (order.name, order.amount_total)
                if order.session_id.state != 'closed':
                    raise UserError('Advertencia!\nLa Sesion %s del TPV %s asociado al Ticket %s el cual esta asociado a la Factura %s no ha sido cerrada, no se pudo realizar la Conciliacion de los Pagos. Primero cierre la sesion para poder correr este proceso.' % (order.session_id.name, order.session_id.config_id.name, order.name, invoice.number))
                if order.state != 'invoiced':
                    continue
                for statement in order.statement_ids:
                    if statement.journal_id.pos_payments_remove_entries or not statement.journal_entry_ids: 
                            continue
                    for account_move in statement.journal_entry_ids:
                        for move_line in account_move.line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('payable', 'receivable')):
                            amls_to_reconcile += move_line
            amls_to_reconcile += invoice.move_id.line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('payable', 'receivable'))
            amls_to_reconcile.reconcile(writeoff_acc_id=False, writeoff_journal_id=False)

        #raise osv.except_osv('Pausa!', 'Pausa')
        return True      
        
        
class pos_order(models.Model):
    _inherit = "pos.order"
    

    def get_customer_for_general_public(self):
        partner_obj = self.env['res.partner']
        partner_id = partner_obj.search([('use_as_general_public','=',1)], limit=1)
        if not partner_id:
            raise UserError(_('Please configure a Partner as default for Use as General Public Partner.'))    

        return partner_id    
    

    
    def action_invoice3(self, date):
        context = self._context
        if 'journal_id' in context:
            journal_id = context['journal_id']    
        else:
            journal_id = False

        #if context is None: self._context = {}
        inv_ref     = self.env['account.move']
        acc_tax_obj = self.env['account.tax']
        inv_line_ref= self.env['account.move.line']
        product_obj = self.env['product.product']
        bsl_obj     = self.env['account.bank.statement.line']
        ### Busqueda del Cliente Publico en General ###
        general_public_partner = self.get_customer_for_general_public()
        tickets_to_set_as_general_public = []

        partner = self.get_customer_for_general_public()
        uom_id = self.env['uom.uom'].search([('use_4_invoice_general_public','=',1)], limit=1)
        if not uom_id:
            raise UserError(_('Please configure a Default Unit of Measure to use as UoM in Invoice Lines.'))
        inv_ids = []
        po_ids = self.env['pos.order']
        lines = {}
        for order in self:
            if order.account_move:
                inv_ids.append(order.account_move.id)
                continue
            if not order.invoice_2_general_public:
                #print "order: %s - %s - %s" % (order.name, order.partner_id and order.partner_id.name or 'Sin Partner', order.invoice_2_general_public)
                res = order.action_pos_order_invoice()
                if res:
                    xinv = inv_ref.browse(res['res_id'])
                    xinv = inv_ref.browse(res['res_id'])
                    if order.session_id.config_id.journal_id:
                        xinv.journal_id = order.session_id.config_id.journal_id.id   
                    xinv.tax_line_ids.set_tax_cash_basis_account()
                    inv_ids.append(res['res_id'])
            else:
               tickets_to_set_as_general_public += order

        if tickets_to_set_as_general_public:
            lines_to_invoice = []
            global_origin_name = ""
            ### Busqueda del Producto para Facturacion ###
            global_product_id = tickets_to_set_as_general_public[0].search_product_global()
            ### Rertorno de la cuenta para Facturación ###
            account = global_product_id.property_account_income_id or global_product_id.categ_id.property_account_income_categ_id
            
            ticket_id_list = []
            for ticket in tickets_to_set_as_general_public:
                pos_reference = ticket.pos_reference if ticket.pos_reference else ticket.name
                global_origin_name += pos_reference+","
                order_line_ids = [x.id for x in ticket.lines]
                if not ticket.global_line_ids:
                    ticket.update_concepts_to_global_invoice()
                for concept in ticket.global_line_ids:
                    lines_to_invoice.append((0,0,{
                            'noidentificacion': pos_reference,
                            'product_id': concept.product_id.id,
                            'name': 'VENTA',
                            'quantity': 1,
                            'account_id': account.id,
                            'uom_id': concept.uom_id.id,
                            'invoice_line_tax_ids': [(6,0,[x.id for x in concept.invoice_line_tax_ids])] if concept.invoice_line_tax_ids else False,
                            'price_unit':concept.price_unit,
                            'discount': 0.0,
                            # 'sale_line_ids': [(6,0,order_line_ids)]
                        }))
                ticket.write({'invoice_2_general_public': True,'state':'invoiced'})

                ### Escribiendo como Facturados los Pedidos ####
                # ticket.order_line.write({'invoice_status' : 'invoiced','invoice_count': 1})
                ticket_id_list.append(ticket.id)
            metodo_pago_id = self.env['sat.metodo.pago'].search([('code','=','PUE')])
            if not metodo_pago_id:
                raise UserError("Error!\nNo se encuentra el metodo de Pago PUE.")
            metodo_pago_id = metodo_pago_id[0]
            uso_cfdi_id = self.env['sat.uso.cfdi'].search([('code','=','P01')])
            if not uso_cfdi_id:
                raise UserError("Error!\nNo se encuentra el uso de cfdi P01.")
            uso_cfdi_id = uso_cfdi_id[0]
            pay_method_ids = self.env['pay.method'].search([('code','=','01')])
            if not pay_method_ids:
                raise UserError("Error!\nNo se encuentra el metodo de Pago 01.")
            pay_method_ids = pay_method_ids[0]

            invoice_vals = {
                    'partner_id': general_public_partner.id,
                    'metodo_pago_id': metodo_pago_id.id,
                    'uso_cfdi_id': uso_cfdi_id.id,
                    'pay_method_ids': [(6,0, [pay_method_ids.id])],
                    'journal_id': journal_id,
                    'invoice_date': date,
                    'invoice_line_ids': lines_to_invoice,
                    'invoice_origin': 'Factura Global [ '+global_origin_name+' ]',

                }

            invoice_id = inv_ref.create(invoice_vals)

            # tickets_to_set_as_general_public.write({'invoice_id': invoice_id.id})
            self.env.cr.execute("""
                update pos_order set account_move = %s where id in %s;
                """,(invoice_id.id, tuple(ticket_id_list)))

            inv_ids.append(invoice_id.id)

            ## Reclasificacando Impuestos ##
            # invoice_id.compute_taxes()
            # invoice_id.tax_line_ids.set_tax_cash_basis_account()

        if not inv_ids: return {}

        return self.action_view_invoice(inv_ids)
        
        
        
        
    def action_view_invoice(self, invoice_ids):
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_move_out_invoice_type')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.view_move_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in', [" + ','.join(map(str, invoice_ids)) + "])]"
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = invoice_ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result


    
class pos_order_invoice_wizard(models.TransientModel):
    _inherit = "pos.order.invoice_wizard"

    def create_invoice_from_pos(self):
        general_public_partner = self.env['pos.order'].get_customer_for_general_public()
        tickets_to_set_as_general_public = ticket_ids = self.env['pos.order']
        res = {}
        for line in self.ticket_ids:
            ticket_ids += line.ticket_id
            if line.invoice_2_general_public:
                tickets_to_set_as_general_public += line.ticket_id
        # Ponemos todos los tickets a facturar como si no fueran Publico en General, esto por si se cancelo/elimino una Factura previa
        
        ticket_ids.write({'invoice_2_general_public': 0})
        #self._cr.execute("update pos_order set invoice_2_general_public=false where id IN %s",(tuple(ids_to_invoice),))
        if tickets_to_set_as_general_public:            
            tickets_to_set_as_general_public.write({'invoice_2_general_public': 1})
            for ticket in tickets_to_set_as_general_public:
                ticket.payment_ids.write({'partner_id': general_public_partner.id})
                # for statement in ticket.payment_ids:
                #     move_ids = [account_move.id for account_move in statement.journal_entry_ids]
                #     if move_ids:
                #         self._cr.execute('update account_move set partner_id=%s where id IN %s;',(general_public_partner.id, tuple(move_ids),))
                #         self._cr.execute('update account_move_line set partner_id=%s where move_id IN %s;',(general_public_partner.id, tuple(move_ids),))
        
        context_to_invoice = {'journal_id': self.journal_id.id }
        res = ticket_ids.with_context(context_to_invoice).action_invoice3(self.date)
        return res or {'type': 'ir.actions.act_window_close'}



class pos_session(models.Model):
    _inherit = "pos.session"
    
    def wkf_action_close(self):
        # Close CashBox
        res = super(pos_session,self).wkf_action_close()
        am_obj = self.env['account.move']
        pos_order_obj = self.env['pos.order']
                
        for record in self:
            for statement in record.statement_ids:
                am_ids = self.env['account.move']
                for statement_line in statement.line_ids:
                    for journal_entry in statement_line.journal_entry_ids:
                        if journal_entry.journal_id.pos_payments_remove_entries:
                            am_id = journal_entry
                            am_ids += am_id
                            if journal_entry.state == 'posted':
                                am_id.button_cancel()
                am_ids.unlink()
            order_ids = pos_order_obj.search([('session_id','=',record.id)])

            if order_ids:
                for order in order_ids:
                    if order.account_move and order.account_move.state == 'draft':
                        order.account_move.post()
        return res        