# -*- coding: utf-8 -*-
# from odoo import http


# class InheritWebExternalLayout(http.Controller):
#     @http.route('/inherit_web_external_layout/inherit_web_external_layout', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_web_external_layout/inherit_web_external_layout/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_web_external_layout.listing', {
#             'root': '/inherit_web_external_layout/inherit_web_external_layout',
#             'objects': http.request.env['inherit_web_external_layout.inherit_web_external_layout'].search([]),
#         })

#     @http.route('/inherit_web_external_layout/inherit_web_external_layout/objects/<model("inherit_web_external_layout.inherit_web_external_layout"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_web_external_layout.object', {
#             'object': obj
#         })
