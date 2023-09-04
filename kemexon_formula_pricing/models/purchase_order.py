from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    show_formula_pricing = fields.Boolean('Show Formula Pricing')



