# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request
class web_delivery_orders(http.Controller):

    @http.route('/delivery-orders-query/load',type="http",website=True,auth='public')
    def estatus_main_seguimiento(self,**kw):
        if request.session.login:
            cliente=request.env['res.partner'].sudo().search([('email','=',request.session.login)])
            if cliente:
                lista_datos=request.env['logistica.ordenes_venta_carga'].sudo().search([('transportista','=',cliente.id)])
                print(lista_datos)
                return http.request.render('logistics_webapp.delivery-order-query',{
                    'lista_datos':lista_datos,
                    })

    @http.route('/delivery-order-query', type='http', website=True, auth='public')
    def delivery_order_query(self, **kw):
        delivery = None
        if kw.get('d_id'):
            delivery = request.env['logistica.ordenes_venta_carga'].sudo().browse(int(kw.get('d_id')))
        partner = request.env.user.partner_id
        return http.request.render('logistics_webapp.portal_delivery_order', {'partner': partner, 'delivery': delivery})

    @http.route('/sumit/delivery/order', type='http', website=True, auth='public')
    def submit_delivery_order(self, **kwargs):
        values = {}
        if kwargs:
            file = kwargs.get('receipt_file')
            delivery_date = kwargs.get('delivery_date')
            platform_number = kwargs.get('platform_number')
            datas = base64.b64encode(file.read())
            lista_datos = request.env['logistica.ordenes_venta_carga'].sudo().browse(int(kwargs.get('d_id')))
            if datas:
                values.update({'evidencia': datas})
            if delivery_date:
                values.update(({'fecha_entrega': delivery_date}))
            if platform_number:
                values.update(({'plataforma': platform_number}))
            if values:
                lista_datos.write(values)

            return http.request.render('logistics_webapp.do_thanking_template')

