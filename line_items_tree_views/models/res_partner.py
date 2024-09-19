from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    res_partner_id = fields.Many2one('res.partner', string='Group', tracking=True)
    short_name = fields.Char(string='Short Name')


    def write(self, vals):
        if 'short_name' in vals:
            if self.search([('short_name', '=', vals['short_name']), ('active', '=', True), ('id', '!=', self.id)]):
                raise ValidationError('Short Name must be unique.')
        return super(ResPartner, self).write(vals)

    def approve(self):
        for contact in self:
            existing_contact = self.search(
                [('short_name', '=', contact.short_name), ('active', '=', True), ('id', '!=', contact.id)])
            if existing_contact:
                raise ValidationError('A contact with the same Short Name already exists.')
            if not self.company_bank_account_id and self.is_company:
                raise ValidationError("Bank is not selected for this partner. Please select a bank before approving.")
        return super(ResPartner, self).approve()




