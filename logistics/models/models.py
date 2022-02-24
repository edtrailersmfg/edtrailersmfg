# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomLogistica(models.Model):
    _name = 'logistica.ordenes_venta_carga'
    # _inherit = 'sale.order'
    _description = "List of Sales Orders and Loading Orders"
    _order = "orden_venta"

    orden_venta = fields.Many2one('sale.order', string='Sales Order', required=True, stored=True)
    cliente = fields.Many2one(related='orden_venta.partner_id', tracking=True, string='Customer',
                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id) )]")
    fecha_pedido = fields.Datetime(related='orden_venta.date_order', tracking=True, string='Order Date')
    fecha_compromiso = fields.Datetime(related='orden_venta.fecha_compromiso', string='Scheduled Shipping Date')
    orden_salida = fields.Many2one('stock.picking', string='Delivery Order')
    fecha_salida = fields.Datetime(string='Departure Date')
    estado = fields.Selection([('N', 'New'), ('T', 'In transit'), ('E', 'Delivered')], string='Delivery Status',
                              track_visibility='onchange')
    evidencia = fields.Binary(string='Evidencia', store=True)
    id_transportista = fields.Many2one('res.partner', string='Carrier',
                                       domain="[('commercial_partner_id', '=', cliente)]")
    # nombre = fields.Char(related='id_transportista.display_name', string='nombre transportista',
    #                      domain="[('name', '=', nombre)]")
    # transportista = fields.Boolean(related='id_transportista.transportista',
    #                                string='Transportista',
    #                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id) )]")
    transportista = fields.Many2one(related='id_transportista.transportista',
                                   string='Carrier')
    fecha_entrega = fields.Datetime(string='Delivery Date')

    _sql_constraints = [

        ('orden_venta_unico', 'unique (orden_venta)', "Error : There can't be duplicate sales orders."),
    ]

    # Al cambiar la orden_venta se actualiza el campo de transportista
    @api.onchange('orden_venta')
    def set_transportista(self):
        for rec in self:
            if rec.cliente:
                rec.id_transportista = rec.cliente
                # print('id_transportista', rec.id_transportista)
                # print('cliente', rec.cliente)
                # print('transportista', rec.transportista)

    def editar_formulario(self):
        view_id = self.env.ref('Logistica.view_logistica_ordenes_venta_carga_form').id
        context = self._context.copy()
        return {
            'name': 'view.logistica.ordenes.venta.carga.form',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'logistica.ordenes_venta_carga',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }

    def crear_formulario(self):
        vals = {
            'orden_venta': self.orden_venta,
            'cliente': self.cliente,
            'fecha_pedido': self.fecha_pedido,
            'fecha_compromiso': self.fecha_compromiso,
            'orden_salida': self.orden_salida,
            'fecha_salida': self.fecha_salida,
            'estado': self.estado,
            'evidencia': self.evidencia,
            'id_transportista': self.id_transportista,
            'transportista': self.transportista,
            'fecha_entrega': self.fecha_entrega,

        }
        return vals

    @api.onchange('fecha_salida')
    def comparar_fecha_salida(self):
        start_date = self.fecha_pedido
        end_date = self.fecha_salida
        if start_date > end_date:
            self.fecha_salida = ''
            raise ValidationError("The departure date must be later than the order date")
        pass

    @api.onchange('fecha_entrega')
    def comparar_fecha_entrega(self):
        start_date = self.fecha_salida
        end_date = self.fecha_entrega
        if start_date > end_date:
            self.fecha_entrega = ''
            raise ValidationError("The delivery date must be after the departure date")
        pass


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    fecha_compromiso = fields.Datetime(string='Scheduled Shipping Date')


class CustomContact(models.Model):
    _inherit = 'res.partner'

    transportista = fields.Boolean(string='Carrier')
