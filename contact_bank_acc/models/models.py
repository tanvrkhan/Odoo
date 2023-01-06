# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_bank_account_id = fields.Many2one('res.partner.bank', 'Company Bank Account')
