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
    ref_no = fields.Char(related='fi_lc_ids.ref_no', string='Reference')
    type = fields.Selection(related='fi_lc_ids.type', string='Type')
    lc_type = fields.Selection(related='fi_lc_ids.lc_type', string='LC Type')
    issuance_date = fields.Date(related='fi_lc_ids.issuance_date', string='Issuance Date')
    expiry_date = fields.Date(related='fi_lc_ids.expiry_date', string='Expiry Date')
    beneficiary = fields.Many2one(related='fi_lc_ids.beneficiary', string='Beneficiary')
    beneficiary_bank = fields.Many2one(related='fi_lc_ids.beneficiary_bank', string='Beneficiary Bank')
    beneficiary_bank_reference = fields.Char(related='fi_lc_ids.beneficiary_bank_reference',
                                             string='Beneficiary Bank Reference')
    applicant = fields.Many2one(related='fi_lc_ids.applicant', string='Applicant')
    applicant_bank = fields.Many2one(related='fi_lc_ids.applicant_bank', string='Applicant Bank')
    applicant_bank_reference = fields.Char(related='fi_lc_ids.applicant_bank_reference',
                                           string='Applicant Bank Reference')
    advising_confirming_bank = fields.Many2one(related='fi_lc_ids.advising_confirming_bank',
                                               string='Advising/Confirming Bank')
    notes = fields.Html(related='fi_lc_ids.notes', string='Notes')
    currency_id = fields.Many2one(related='fi_lc_ids.currency_id', string='Currency')
    total_quantity = fields.Float(related='fi_lc_ids.total_quantity', string='Total Quantity')
    total_amount = fields.Monetary(related='fi_lc_ids.total_amount', string='Total Amount',
                                   currency_field='currency_id')
    company_id = fields.Many2one(related='fi_lc_ids.company_id', string='Company')

    @api.depends('unit_price', 'quantity')
    def _compute_amount(self):
        for line in self:
            line.amount = line.unit_price*line.quantity

