# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class web_delivery_orders(http.Controller):

    @http.route('/deliveryorders/my',type="http",website=True,auth='public')
    def estatus_main_seguimiento(self,**kw):
        return http.request.render('estatus_web.consulta_estatus_personas')


