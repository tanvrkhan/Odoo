# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import base64
from operator import itemgetter


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_bank_account_id = fields.Many2one('res.partner.bank', 'Company Bank Account')
