# -*- coding: utf-8 -*-
# from odoo import http


# class ProfitLossView(http.Controller):
#     @http.route('/profit_loss_view/profit_loss_view', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/profit_loss_view/profit_loss_view/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('profit_loss_view.listing', {
#             'root': '/profit_loss_view/profit_loss_view',
#             'objects': http.request.env['profit_loss_view.profit_loss_view'].search([]),
#         })

#     @http.route('/profit_loss_view/profit_loss_view/objects/<model("profit_loss_view.profit_loss_view"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('profit_loss_view.object', {
#             'object': obj
#         })
