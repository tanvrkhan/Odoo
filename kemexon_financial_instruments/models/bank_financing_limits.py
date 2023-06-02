from odoo import models, fields, api


class BankFinancingLimits(models.Model):
    _name = 'bank.financing.limits'
    _description = 'Bank Financing Limits'

    bank_id = fields.Integer('Bank ID')
    limit_name = fields.Char('Limit Name')
    amount = fields.Float('Amount')
    bank_view_ids = fields.Many2one('res.bank', string="Financing Limits")


class ResBank(models.Model):
    _inherit = 'res.bank'

    bank_financing_limits_ids = fields.One2many('bank.financing.limits', 'bank_view_ids', string="Financing Limits")
    notes = fields.Html(string='Notes')
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount')

    @api.depends('bank_financing_limits_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.bank_financing_limits_ids)


