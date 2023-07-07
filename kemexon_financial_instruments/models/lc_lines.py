from odoo import api, fields, models, _


class LcLines(models.Model):
    _name = 'lc.lines'
    _description = 'LC Lines'

    product = fields.Many2one('product.product', string='Product')
    product_family = fields.Char(string='Product Family')
    quantity = fields.Float(string='Quantity')
    tolerance_type = fields.Selection([
        ('min_max', 'Min/Max'),
        ('max', 'Max'),
        ('min', 'Min')
    ], string='Tolerance Type')
    tolerance_percentage = fields.Float(string='Tolerance Percentage')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Monetary(string='Amount', readonly=True, currency_field='currency_id', compute='_compute_amount')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fi_lc_ids = fields.Many2one('fi.lc', string="LC Lines")

    # @api.onchange('unit_price', 'quantity')
    # def _onchange_unit_price_quantity(self):
    #     self.amount = self.unit_price * self.quantity

    @api.depends('unit_price', 'quantity')
    def _compute_amount(self):
        for line in self:
            line.amount = line.unit_price*line.quantity

