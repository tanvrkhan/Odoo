from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Region(models.Model):
    _name = 'region.region'
    _description = 'Region'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'region_name'

    region_name = fields.Char(string='Name', required=True)
    notes = fields.Html(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.constrains('region_name')
    def _check_unique_region_name(self):
        for record in self:
            if record.search([('region_name', '=', record.region_name), ('id', '!=', record.id)]):
                raise ValidationError('Region name must be unique!')

