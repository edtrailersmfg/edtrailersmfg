# -*- coding: utf-8 -*-
# from odoo import http


# class Logistica(http.Controller):
#     @http.route('/logistica/logistica', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/logistica/logistica/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('logistica.listing', {
#             'root': '/logistica/logistica',
#             'objects': http.request.env['logistica.logistica'].search([]),
#         })

#     @http.route('/logistica/logistica/objects/<model("logistica.logistica"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('logistica.object', {
#             'object': obj
#         })
