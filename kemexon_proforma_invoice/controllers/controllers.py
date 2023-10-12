# -*- coding: utf-8 -*-
# from odoo import http


# class KemexonProformaInvoice(http.Controller):
#     @http.route('/kemexon_proforma_invoice/kemexon_proforma_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kemexon_proforma_invoice/kemexon_proforma_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kemexon_proforma_invoice.listing', {
#             'root': '/kemexon_proforma_invoice/kemexon_proforma_invoice',
#             'objects': http.request.env['kemexon_proforma_invoice.kemexon_proforma_invoice'].search([]),
#         })

#     @http.route('/kemexon_proforma_invoice/kemexon_proforma_invoice/objects/<model("kemexon_proforma_invoice.kemexon_proforma_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kemexon_proforma_invoice.object', {
#             'object': obj
#         })
