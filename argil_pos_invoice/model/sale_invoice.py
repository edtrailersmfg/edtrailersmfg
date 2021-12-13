# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

    
class sale_order(models.Model):
    _inherit = "sale.order"
    
    
    invoice_2_general_public = fields.Boolean(string='Publico en General', 
                                              help="Check this if this POS Ticket will be invoiced as General Public")
    
    def get_customer_for_general_public(self):
        partner_obj = self.env['res.partner']
        partner_id = partner_obj.search([('use_as_general_public','=',1)], limit=1)
        if not partner_id:
            raise UserError(_('Por favor, configura un cliente como Publico en General.'))    

        return partner_id    
    

class sale_order_invoice_wizard(models.TransientModel):
    _name = "sale.order.invoice_wizard"
    _description = "Wizard to create Invoices from several Sale Tickets"


    @api.model  
    def default_get(self, fields):
        res = super(sale_order_invoice_wizard, self).default_get(fields)
        record_ids = self._context.get('active_ids', [])
        sale_order_obj = self.env['sale.order']
        if not record_ids:
            return {}
        tickets = []
        
        partner_id = sale_order_obj.get_customer_for_general_public().id
        
        for ticket in sale_order_obj.browse(record_ids):
            
            if ticket.state in ('cancel') or ticket.invoice_status != 'to invoice':
                continue
            # flag = not bool(ticket.partner_id) or bool(ticket.partner_id.invoice_2_general_public or ticket.partner_id.id == partner_id) or False
            flag = False
            if self.env.user.company_id.invoice_public_default:
                flag = True
            else:
                flag = not bool(ticket.partner_id) or bool(ticket.partner_id.invoice_2_general_public or ticket.partner_id.id == partner_id) or False
            
            tickets.append((0,0,{
                    'ticket_id'     : ticket.id,
                    'date_order'    : ticket.date_order,
                    'sale_reference' : ticket.name,
                    'user_id'       : ticket.user_id.id,
                    'partner_id'    : ticket.partner_id and ticket.partner_id.id or False,
                    'amount_total'  : ticket.amount_total,
                    'invoice_2_general_public' : flag,
                    }))
        res.update(ticket_ids=tickets)
        return res


    date       = fields.Datetime(string='Fecha', default=fields.Datetime.now(), required=True,
                              help='This date will be used as the invoice date and period will be chosen accordingly!')
    journal_id = fields.Many2one('account.journal', string='Diario Facturacion', required=True,
                                  default=lambda self: self.env['account.journal'].search([('type', '=', 'sale'), ('company_id','=',self.env.user.company_id.id)], limit=1),
                                  help='You can select here the journal to use for the Invoice that will be created.')
    ticket_ids = fields.One2many('sale.order.invoice_wizard.line','wiz_id',string='Ventas a Facturar', required=True)



    def create_invoice_from_sales(self):
        invoice_obj = self.env['account.move']
        invoice_ids = []
        ### Busqueda del Cliente Publico en General ###
        general_public_partner = self.env['sale.order'].get_customer_for_general_public()
        tickets_to_set_as_general_public = []

        tickets_simple_invoice =  []
        res = {}
        for line in self.ticket_ids:
            if line.invoice_2_general_public:
                tickets_to_set_as_general_public += line.ticket_id
            else:
                tickets_simple_invoice.append(line.ticket_id)
            
        # Ponemos todos los tickets a facturar como si no fueran Publico en General, esto por si se cancelo/elimino una Factura previa
        
        if tickets_to_set_as_general_public:
            lines_to_invoice = []
            global_origin_name = ""
            ### Busqueda del Producto para Facturacion ###
            global_product_id = tickets_to_set_as_general_public[0].search_product_global()
            ### Rertorno de la cuenta para Facturación ###
            account = global_product_id.property_account_income_id or global_product_id.categ_id.property_account_income_categ_id
            if not account:
                raise UserError(_('Por favor crea una cuenta para el producto: "%s" (id:%d) - or for its category: "%s".') %
                    (global_product_id.name, global_product_id.id, global_product_id.categ_id.name))

            fpos = tickets_to_set_as_general_public[0].fiscal_position_id or tickets_to_set_as_general_public[0].partner_id.property_account_position_id
            if fpos:
                account = fpos.map_account(account)

            ticket_id_list = []
            for ticket in tickets_to_set_as_general_public:
                global_origin_name += ticket.name+","
                order_line_ids = [x.id for x in ticket.order_line]
                if not ticket.global_line_ids:
                    ticket.update_concepts_to_global_invoice()
                for concept in ticket.global_line_ids:
                    lines_to_invoice.append((0,0,{
                            'noidentificacion': ticket.name,
                            'product_id': concept.product_id.id,
                            'name': 'VENTA',
                            'quantity': 1,
                            'account_id': account.id,
                            'uom_id': concept.uom_id.id,
                            'invoice_line_tax_ids': [(6,0,[x.id for x in concept.invoice_line_tax_ids])] if concept.invoice_line_tax_ids else False,
                            'price_unit':concept.price_unit,
                            'discount': 0.0,
                            #'sale_line_ids': [(6,0,order_line_ids)]
                        }))
                ticket.write({'invoice_2_general_public': True})

                ### Escribiendo como Facturados los Pedidos ####
                ticket.order_line.write({'invoice_status' : 'invoiced'})
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
                'journal_id': self.journal_id.id,
                'date_invoice': self.date,
                'invoice_line_ids': lines_to_invoice,
                'origin': 'Factura Global [ '+global_origin_name+' ]',

            }

            invoice_id = invoice_obj.create(invoice_vals)
            invoice_ids.append(invoice_id.id)
            ### Grabar Facturas #####
            self.env['sale.order'].browse(ticket_id_list).write({'invoice_global_ids': [(6,0,[invoice_id.id])], 'invoice_status': 'invoiced', 'invoice_count': 1 })
            # self.env['sale.order'].browse(ticket_id_list)._get_invoiced()

            # self.env.cr.execute("""
            #     update sale_order_line set invoice_id = %s where order_id in %s;
            #     """, (invoice_id.id, tuple(ticket_id_list),))
        if tickets_simple_invoice:
            for ticket in tickets_simple_invoice:
                invoice_id = ticket.action_invoice_create()
                invoice_ids.append(invoice_id[0])

        ### Rertorno de la información ###
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        return {
                    'domain': [('id', 'in', invoice_ids)],
                    'name': _('Factura Global'),
                    'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
                    'target': action.target,
                    'context': action.context,
                    'res_model': 'account.move',
                    'type': 'ir.actions.act_window'
                    }
        

        
class sale_order_invoice_wizard_line(models.TransientModel):
    _name = "sale.order.invoice_wizard.line"
    _description = "Wizard to create Invoices from several POS Tickets2"

    wiz_id        = fields.Many2one('sale.order.invoice_wizard',string='ID Return', ondelete="cascade")
    ticket_id     = fields.Many2one('sale.order', string='Venta')
    date_order    = fields.Datetime(related='ticket_id.date_order', string="Fecha", readonly=True)
    sale_reference = fields.Char(related='ticket_id.name', string="Referencia", readonly=True)
    user_id       = fields.Many2one("res.users", related='ticket_id.user_id', string="Vendedor", readonly=True)
    amount_total  = fields.Float("Total", readonly=True)
    partner_id    = fields.Many2one("res.partner", related='ticket_id.partner_id', string="Cliente", readonly=True)
    invoice_2_general_public = fields.Boolean('Publico en General')
        

