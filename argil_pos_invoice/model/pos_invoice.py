# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

    
class pos_order(models.Model):
    _inherit = "pos.order"
    
    
    invoice_2_general_public = fields.Boolean(string='General Public', 
                                              help="Check this if this POS Ticket will be invoiced as General Public")


class pos_order_invoice_wizard(models.TransientModel):
    _name = "pos.order.invoice_wizard"
    _description = "Wizard to create Invoices from several POS Tickets"



    @api.model  
    def default_get(self, fields):
        # print "######## fields >>>>>>>> ",fields
        # res = super(sale_order_invoice_wizard, self).default_get(fields)

        # res.update(ticket_ids=tickets)
        contextual_self = self.with_context(default_load_tickets=True)
        res = super(pos_order_invoice_wizard, contextual_self).default_get(fields)
        record_ids = self._context.get('active_ids', [])
        pos_order_obj = self.env['pos.order']
        if not record_ids:
            return {}
        tickets = []
        
        partner_id = pos_order_obj.get_customer_for_general_public().id
        
        for ticket in pos_order_obj.browse(record_ids):
            
            if ticket.state in ('cancel','draft') or (ticket.account_move and ticket.account_move.state != 'cancel'):
                continue
            #flag = not bool(ticket.partner_id) or bool(ticket.partner_id.invoice_2_general_public or ticket.partner_id.id == partner_id) or False
            flag = False
            if self.env.user.company_id.invoice_public_default:
                flag = True
            else:
                flag = not bool(ticket.partner_id) or bool(ticket.partner_id.invoice_2_general_public or ticket.partner_id.id == partner_id) or False
            tickets.append((0,0,{
                    'ticket_id'     : ticket.id,
                    'date_order'    : ticket.date_order,
                    'session_id'    : ticket.session_id.id,
                    'pos_reference' : ticket.pos_reference if ticket.pos_reference else ticket.name,
                    'user_id'       : ticket.user_id.id,
                    'partner_id'    : ticket.partner_id and ticket.partner_id.id or False,
                    'amount_total'  : ticket.amount_total,
                    'invoice_2_general_public' : flag,
                    'invoice_2_general_public_copy' : flag,
                    }))
        res.update({'ticket_ids': tickets})


        # res.update({'ticket_ids': tickets})
        # print "########## res >>>>>>>>> ",res
        return res



    date       = fields.Datetime(string='Date', default=fields.Datetime.now(), required=True,
                              help='This date will be used as the invoice date and period will be chosen accordingly!')
    journal_id = fields.Many2one('account.journal', string='Invoice Journal', required=True,
                                  default=lambda self: self.env['account.journal'].search([('type', '=', 'sale'), ('company_id','=',self.env.user.company_id.id)], limit=1),
                                  help='You can select here the journal to use for the Invoice that will be created.')
    ticket_ids = fields.One2many('pos.order.invoice_wizard.line','wiz_id',string='Tickets to Invoice', required=True)
    load_tickets = fields.Boolean('Cargar Tickets', default=True)


    # @api.onchange('load_tickets','date','journal_id')
    # def onchange_load_tickets(self):
    #     record_ids = self._context.get('active_ids', [])
    #     pos_order_obj = self.env['pos.order']
    #     if not record_ids:
    #         return {}
    #     tickets = []
        
    #     partner_id = pos_order_obj.get_customer_for_general_public().id
        
    #     for ticket in pos_order_obj.browse(record_ids):
            
    #         if ticket.state in ('cancel','draft') or (ticket.invoice_id and ticket.invoice_id.state != 'cancel'):
    #             continue
    #         flag = not bool(ticket.partner_id) or bool(ticket.partner_id.invoice_2_general_public or ticket.partner_id.id == partner_id) or False
    #         tickets.append((0,0,{
    #                 'ticket_id'     : ticket.id,
    #                 'date_order'    : ticket.date_order,
    #                 'session_id'    : ticket.session_id.id,
    #                 'pos_reference' : ticket.pos_reference if ticket.pos_reference else ticket.name,
    #                 'user_id'       : ticket.user_id.id,
    #                 'partner_id'    : ticket.partner_id and ticket.partner_id.id or False,
    #                 'amount_total'  : ticket.amount_total,
    #                 'invoice_2_general_public' : flag,
    #                 'invoice_2_general_public_copy' : flag,
    #                 }))
    #     self.ticket_ids = tickets

        
class pos_order_invoice_wizard_line(models.TransientModel):
    _name = "pos.order.invoice_wizard.line"
    _description = "Wizard to create Invoices from several POS Tickets2"

    wiz_id        = fields.Many2one('pos.order.invoice_wizard',string='Wizard', ondelete="cascade")
    ticket_id     = fields.Many2one('pos.order', string='POS Ticket')
    date_order    = fields.Datetime(related='ticket_id.date_order', string="Date", readonly=True)
    session_id    = fields.Many2one("pos.session", related='ticket_id.session_id', string="Session", readonly=True)
    pos_reference = fields.Char(related='ticket_id.pos_reference', string="Reference", readonly=True)
    user_id       = fields.Many2one("res.users", related='ticket_id.user_id', string="Salesman", readonly=True)
    amount_total  = fields.Float(related='ticket_id.amount_total', string="Total", readonly=True)
    partner_id    = fields.Many2one("res.partner", related='ticket_id.partner_id', string="Partner", readonly=True)
    invoice_2_general_public = fields.Boolean('General Public')
    invoice_2_general_public_copy = fields.Boolean('General Public')


    @api.onchange('invoice_2_general_public_copy')
    def onchange_metodo(self):
        self.invoice_2_general_public = self.invoice_2_general_public_copy
    
        

