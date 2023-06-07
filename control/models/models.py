# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class Control(models.Model):
    _name = 'control.control'
    _inherit = ["portal.mixin","mail.thread","mail.activity.mixin"]
    _description = "Lista de Control de la Produccion"
    _order = "orden_venta"

    def compute_name(self):
        self.name = self.serie.name
    order       = fields.Integer(defaul=10, help="Campo para ordenar los registros de acuerdo a la produccion")
    orden_venta = fields.Many2one('sale.order', string='Orden de Venta', stored=True)
    cliente     = fields.Many2one(related='orden_venta.partner_id', tracking=True, string='Cliente',
                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id) )]")
    fecha_orden      = fields.Datetime(related='orden_venta.date_order', tracking=True, string='Fecha Orden', store=True)
    fecha_compromiso = fields.Datetime(related='orden_venta.fecha_compromiso', string='Fecha Compromiso', store=True)
    orden_produccion = fields.Many2one('mrp.production', string="Producción", stored=True)
    producto         = fields.Many2one(related='orden_produccion.product_id', string="Producto", stored=True)
    serie            = fields.Many2one(related='orden_produccion.lot_producing_id', string="Serie", stored=True)
    name             = fields.Char(string="name", compute="compute_name")
    centro_trabajo = fields.Selection([
                ('No Iniciado','No Iniciado'),
                ('Producción','Producción'),
                ('Pintura','Pintura'),
                ('Ensamble','Ensamble'),
                ('Terminado','Terminado'),
                ('Hold','Hold'),
            ], string='Centro de Trabajo', 
               default='No Iniciado'
        )
    terminado = fields.Boolean(string='Terminado')
    hold = fields.Boolean(string='Hold')

    #agregar fecha de inicio, fecha final y nombre del producto
    fecha_inicio   = fields.Datetime(string='Fecha Inicio')
    fecha_fin      = fields.Datetime(string='Fecha Fin')

