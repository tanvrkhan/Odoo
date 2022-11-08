# -*- coding: utf-8 -*-
# from odoo import http


# class ContactsImportAdditionalFields(http.Controller):
#     @http.route('/contacts_import_additional_fields/contacts_import_additional_fields', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contacts_import_additional_fields/contacts_import_additional_fields/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contacts_import_additional_fields.listing', {
#             'root': '/contacts_import_additional_fields/contacts_import_additional_fields',
#             'objects': http.request.env['contacts_import_additional_fields.contacts_import_additional_fields'].search([]),
#         })

#     @http.route('/contacts_import_additional_fields/contacts_import_additional_fields/objects/<model("contacts_import_additional_fields.contacts_import_additional_fields"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contacts_import_additional_fields.object', {
#             'object': obj
#         })
