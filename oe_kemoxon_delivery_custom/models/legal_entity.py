from odoo import models, fields

class LegalEntity(models.Model):
    _name = 'legal.entity'
    _description = 'Legal Entity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Entity Name', required=True)
    registration_number = fields.Char(string='Registration Number')
    incorporation_date = fields.Date(string='Incorporation Date')
    country_id = fields.Many2one('res.country', string='Country')
    vat_id = fields.Char('VAT ID')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
