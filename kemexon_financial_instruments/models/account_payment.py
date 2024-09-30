from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    fi_lc_id = fields.Many2one('fi.lc', string='Financial Instrument Ref')
    loan_ref = fields.Char(string='Loan Ref')
    loan_expiry_date = fields.Date(string='Loan Expiry Date')
