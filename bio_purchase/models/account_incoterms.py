# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class AccountIncoterms(models.Model):
    _inherit = "account.incoterms"
    _rec_name = "code"
