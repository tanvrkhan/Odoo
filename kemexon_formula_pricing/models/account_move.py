from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    show_formula_pricing = fields.Boolean('Show Formula Pricing')

