from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_formula_pricing = fields.Boolean('Formula Pricing')
    formula_price = fields.Float('Formula Price', digits=(6, 3))
    premium = fields.Float('Premium', digits=(6, 3))
    formula_description = fields.Char('Formula Description')

    @api.onchange('is_formula_pricing', 'premium', 'formula_price')
    def _compute_price_unit_aml(self):
        for line in self:
            if line.is_formula_pricing:
                line.price_unit = line.formula_price + line.premium
            else:
                line.price_unit = 0


