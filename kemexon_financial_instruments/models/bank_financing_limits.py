from odoo import models, fields, api


class BankFinancingLimits(models.Model):
    _name = 'bank.financing.limits'
    _description = 'Bank Financing Limits'
    _rec_name = 'limit_name'
    
    bank_id = fields.Many2one('res.bank',required =True)
    limit_name = fields.Char('Limit Name')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

   
class ResBank(models.Model):
    _inherit = 'res.bank'

    bank_financing_limits_ids = fields.One2many('bank.financing.limits', 'bank_id', string="Financing Limits")
    notes = fields.Html(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id')

    @api.depends('bank_financing_limits_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.bank_financing_limits_ids)


