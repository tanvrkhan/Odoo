# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contacts_import_additional_fields(models.Model):
    _inherit='res.partner'
    short_name=fields.Char(required=True)
#     _description = 'contacts_import_additional_fields.contacts_import_additional_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
