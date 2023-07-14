from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IncotermLocation(models.Model):
    _name = 'incoterm.location'
    _description = 'Incoterm Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    region = fields.Many2one('region.region', string='Region')
    country = fields.Many2one('res.country', string='Country')
    notes = fields.Html(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError('Name must be unique!')
