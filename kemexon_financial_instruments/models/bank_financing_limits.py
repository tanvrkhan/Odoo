from odoo import models, fields, api


class BankFinancingLimits(models.Model):
    _name = 'bank.financing.limits'
    _description = 'Bank Financing Limits'

    bank_id = fields.Integer('Bank ID')
    limit_name = fields.Char('Limit Name')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    bank_view_ids = fields.Many2one('res.bank', string="Financing Limits")


class ResBank(models.Model):
    _inherit = 'res.bank'

    bank_financing_limits_ids = fields.One2many('bank.financing.limits', 'bank_view_ids', string="Financing Limits")
    notes = fields.Html(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id')

    @api.depends('bank_financing_limits_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.bank_financing_limits_ids)


