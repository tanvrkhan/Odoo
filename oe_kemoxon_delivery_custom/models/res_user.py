from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    custom_categ_id = fields.Many2many('product.category', string='Product Category', store=True)