from odoo import api, fields, models, _


class LcLines(models.Model):
    _name = 'fi.lc.lines'
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
    fi_lc_id = fields.Many2one('fi.lc', string="LC Lines")
    ref_no = fields.Char(related='fi_lc_id.ref_no', string='Reference', store=True)
    type = fields.Selection(related='fi_lc_id.type', string='Type', store=True)
    lc_type = fields.Selection(related='fi_lc_id.lc_type', string='LC Type', store=True)
    sub_limit = fields.Many2one('bank.financing.limits',related='fi_lc_id.sub_limit', string='Sub Limit', store=True)
    issuance_date = fields.Date(related='fi_lc_id.issuance_date', string='Issuance Date', store=True)
    expiry_date = fields.Date(related='fi_lc_id.expiry_date', string='Expiry Date', store=True)
    is_active = fields.Boolean(related='fi_lc_id.is_active', string='Is Active', store=True)
    beneficiary = fields.Many2one(related='fi_lc_id.beneficiary', string='Beneficiary', store=True)
    beneficiary_bank = fields.Many2one(related='fi_lc_id.beneficiary_bank', string='Beneficiary Bank')
    beneficiary_bank_reference = fields.Char(related='fi_lc_id.beneficiary_bank_reference',
                                             string='Beneficiary Bank Reference')
    applicant = fields.Many2one(related='fi_lc_id.applicant', string='Applicant')
    applicant_bank = fields.Many2one(related='fi_lc_id.applicant_bank', string='Applicant Bank')
    applicant_bank_reference = fields.Char(related='fi_lc_id.applicant_bank_reference',
                                           string='Applicant Bank Reference')
    advising_confirming_bank = fields.Many2one(related='fi_lc_id.advising_confirming_bank',
                                               string='Advising/Confirming Bank')
    notes = fields.Html(related='fi_lc_id.notes', string='Notes')
    total_quantity = fields.Float(related='fi_lc_id.total_quantity', string='Total Quantity')
    total_amount = fields.Monetary(related='fi_lc_id.total_amount', string='Total Amount',
                                   currency_field='currency_id')
    company_id = fields.Many2one(related='fi_lc_id.company_id', string='Company')

    @api.depends('unit_price', 'quantity')
    def _compute_amount(self):
        for line in self:
            line.amount = line.unit_price*line.quantity

