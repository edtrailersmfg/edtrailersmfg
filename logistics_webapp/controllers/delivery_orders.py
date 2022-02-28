# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class web_delivery_orders(http.Controller):

    @http.route('/delivery-orders-query/load',type="http",website=True,auth='public')
    def estatus_main_seguimiento(self,**kw):
        return http.request.render('estatus_web.consulta_estatus_personas')


    @http.route('/delivery-orders-query',type="http",website=True,auth='public')
    def estatus_siguimiento(self, **kw):
        lista_datos=request.env['res.partner'].sudo().search([('x_id','=',kw.get('folio'))])
        print(lista_datos)
        return http.request.render('estatus_web.consulta_estatus_personas',{
         'lista_datos':lista_datos,
        })

