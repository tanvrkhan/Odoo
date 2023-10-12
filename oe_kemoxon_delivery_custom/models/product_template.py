from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_code_custom = fields.Char('HS Code')
