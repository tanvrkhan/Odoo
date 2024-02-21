# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    vessel_owner = fields.Boolean()
    inspector = fields.Boolean()
    transporter = fields.Boolean()
    receiver = fields.Boolean()
    agent = fields.Boolean()
    broker = fields.Boolean()
    # information vessel
    vessel_ids = fields.One2many(
        'bio.vessel', 'partner_id', string='Vessels')
    vessel_count = fields.Integer(compute='_compute_vessel_ids')

    @api.depends('vessel_ids')
    def _compute_vessel_ids(self):
        for record in self:
            record.vessel_count = len(record.vessel_ids)
