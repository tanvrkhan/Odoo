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
    issuance_date = fields.Date(string='Issuance Date')
    expiry_date = fields.Date(string='Expiry Date')
    beneficiary = fields.Many2one('res.partner', string='Beneficiary')
    beneficiary_bank = fields.Many2one('res.bank', string='Beneficiary Bank')
    beneficiary_bank_reference = fields.Char(string='Beneficiary Bank Reference')
    applicant = fields.Many2one('res.partner', string='Applicant')
    applicant_bank = fields.Many2one('res.bank', string='Applicant Bank')
    applicant_bank_reference = fields.Char(string='Applicant Bank Reference')
    advising_confirming_bank = fields.Many2one('res.bank', string='Advising/Confirming Bank')
    notes = fields.Html(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    lc_lines_ids = fields.One2many("lc.lines", 'fi_lc_ids', string="LC Lines")
    total_quantity = fields.Float(compute='_compute_total_quantity', string='Total Quantity')
    total_amount = fields.Monetary(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id')

    @api.depends('lc_lines_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.lc_lines_ids)

    @api.depends('lc_lines_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.lc_lines_ids)

    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for record in self:
            if record.expiry_date and record.expiry_date < record.issuance_date:
                raise ValidationError("Expiry Date must be equal to or greater than the Issuance Date!")

    @api.constrains('ref_no')
    def _check_unique_ref_no(self):
        for record in self:
            if record.search([('ref_no', '=', record.ref_no), ('id', '!=', record.id)]):
                raise ValidationError('Reference must be unique!')