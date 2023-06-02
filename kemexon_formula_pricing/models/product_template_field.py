from odoo import fields, models, api


class ProductTemplateField(models.Model):
    _inherit = 'product.template'

    m2m_price = fields.Float('M2M')
    mt_factor = fields.Float('MT Factor')
