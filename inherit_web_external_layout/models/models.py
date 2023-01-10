# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class inherit_web_external_layout(models.Model):
#     _name = 'inherit_web_external_layout.inherit_web_external_layout'
#     _description = 'inherit_web_external_layout.inherit_web_external_layout'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
