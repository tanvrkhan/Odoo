# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class UoM(models.Model):
    _inherit = 'uom.uom'

    is_business = fields.Boolean("")
