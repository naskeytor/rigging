# -*- coding: utf-8 -*-
# from odoo import http


# class Rigging(http.Controller):
#     @http.route('/rigging/rigging', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rigging/rigging/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rigging.listing', {
#             'root': '/rigging/rigging',
#             'objects': http.request.env['rigging.rigging'].search([]),
#         })

#     @http.route('/rigging/rigging/objects/<model("rigging.rigging"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rigging.object', {
#             'object': obj
#         })
