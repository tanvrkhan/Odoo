from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_formula_pricing = fields.Boolean('Show Formula Pricing')
    valid_until = fields.Date('Valid until')
    show_validity = fields.Boolean('Show validity')
