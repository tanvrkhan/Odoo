from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_formula_pricing = fields.Boolean('Show Formula Pricing')

