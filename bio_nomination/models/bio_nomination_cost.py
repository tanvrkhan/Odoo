# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BioNominationCost(models.Model):
    _name = "bio.nomination.cost"
    _description = "Bio cost"
    name = fields.Many2one('bio.nomination.cost.type', required=1)
    price = fields.Float()
    qty = fields.Integer()
    uom_id = fields.Many2one('uom.uom')
    currency_id = fields.Many2one('res.currency')
    nomination_id = fields.Many2one('bio.nomination')
