from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FiLc(models.Model):
    _name = 'fi.lc'
    _description = 'Financial LC'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref_no'

    ref_no = fields.Char('Reference', required=True)
    type = fields.Selection([('sblc', 'SBLC'), ('lc', 'LC')], string="Type")
    lc_type = fields.Selection([('import', 'Import(Purchase)'), ('export', 'Export(Sale)')], string="LC Type")
    sub_limit = fields.Many2one('bank.financing.limits', string='Sub limit')

    issuance_date = fields.Date(string='Issuance Date')
    expiry_date = fields.Date(string='Expiry Date')
    is_active = fields.Boolean(string='Is Active')
    beneficiary = fields.Many2one('res.partner', string='Beneficiary')
    beneficiary_bank = fields.Many2one('res.bank', string='Beneficiary Bank')
    beneficiary_bank_reference = fields.Char(string='Beneficiary Bank Reference')
    applicant = fields.Many2one('res.partner', string='Applicant')
    applicant_bank = fields.Many2one('res.bank', string='Applicant Bank')
    applicant_bank_reference = fields.Char(string='Applicant Bank Reference')
    advising_confirming_bank = fields.Many2one('res.bank', string='Advising/Confirming Bank')
    notes = fields.Html(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fi_lc_line_ids = fields.One2many("fi.lc.lines", 'fi_lc_id', string="LC Lines")
    total_quantity = fields.Float(compute='_compute_total_quantity', string='Total Quantity',stored=True)
    total_amount = fields.Monetary(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id',stored=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('fi_lc_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.fi_lc_line_ids)
    
    
    @api.depends('fi_lc_line_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.fi_lc_line_ids)

    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for record in self:
            if record.expiry_date and record.expiry_date < record.issuance_date:
                raise ValidationError("Expiry Date must be equal to or greater than the Issuance Date!")

    @api.constrains('ref_no')
    def _check_unique_ref_no(self):
        for record in self:
            # Check for uniqueness only for records that do not end with "(Copy)"
            if not record.ref_no.endswith('(copy)') and record.search([
                ('ref_no', '=', record.ref_no),
                ('id', '!=', record.id)
            ]):
                raise ValidationError('Reference must be unique!')

    def copy(self, default=None):
        """Override the copy method to append (Copy) to ref_no the first time,
        and subsequent copies of 'Test (Copy)' remain the same."""
        default = dict(default or {})

        # Check if the current ref_no already has "(Copy)" appended
        if "(copy)" not in self.ref_no:
            # If not, append "(Copy)" to the original ref_no
            default['ref_no'] = f"{self.ref_no} (copy)"
        else:
            # If it already contains "(Copy)", keep it the same
            default['ref_no'] = self.ref_no

        return super(FiLc, self).copy(default)