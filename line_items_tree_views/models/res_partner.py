from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    res_partner_id = fields.Many2one('res.partner', string='Group', tracking=True)
    short_name = fields.Char(string='Short Name')

    @api.constrains('short_name')
    def _check_unique_short_name(self):
        for record in self:
            if self.search([('short_name', '=', record.short_name), ('active', '=', True), ('id', '!=', record.id), ('is_company', '=', True), ('name', '!=', record.name)]):
                raise ValidationError('Short Name must be unique.')

    @api.model
    def create(self, vals):
        if self.search([('short_name', '=', vals.get('short_name')), ('active', '=', True), ('id', '!=', vals.get('id')), ('is_company', '=', True), ('name', '!=', vals.get('name'))]):
            raise ValidationError('Short Name must be unique.')
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'short_name' in vals:
            if self.search([('short_name', '=', vals.get('short_name')), ('active', '=', True), ('id', '!=', vals.get('id')), ('is_company', '=', True), ('name', '!=', vals.get('name'))]):
                raise ValidationError('Short Name must be unique.')
        return super(ResPartner, self).write(vals)

    def approve(self):
        for contact in self:
            existing_contact = self.search(
                self.search([('short_name', '=', contact.short_name), ('active', '=', True), ('id', '!=', contact.id), ('is_company', '=', True), ('name', '!=', contact.name)]))
            if existing_contact:
                raise ValidationError('A contact with the same Short Name already exists.')
        return super(ResPartner, self).approve()


