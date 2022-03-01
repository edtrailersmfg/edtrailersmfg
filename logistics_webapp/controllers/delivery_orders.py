# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class web_delivery_orders(http.Controller):

    @http.route('/delivery-orders-query/load',type="http",website=True,auth='public')
    def estatus_main_seguimiento(self,**kw):
        cliente=request.env['res.partner'].sudo().search([('email','=',request.session.login)])
        lista_datos=request.env['logistica.ordenes_venta_carga'].sudo().search([('transportista','=',cliente.id)])
        print(lista_datos)
        return http.request.render('logistics_webapp.delivery-order-query',{
            'lista_datos':lista_datos,
            })





