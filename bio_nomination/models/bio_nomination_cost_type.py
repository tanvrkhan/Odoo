# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BioNominationCostType(models.Model):
    _name = "bio.nomination.cost.type"
    _description = "Bio  cost name"
    name = fields.Char()