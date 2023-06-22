from odoo import fields, models, api


class ProductTemplateField(models.Model):
    _inherit = 'product.template'

    m2m_price = fields.Float('M2M', digits=(6, 3))
    mt_factor = fields.Float('MT Factor', digits=(6, 4))
