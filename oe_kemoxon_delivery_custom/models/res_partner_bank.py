# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import base64


class AccountMove(models.Model):
    _inherit = "res.partner.bank"

    inter_mediatory_bank_id = fields.Many2one('res.bank', 'Intermediary Bank')
    inter_mediatory_swift = fields.Char(string='Intermediary Swift', related='inter_mediatory_bank_id.bic')




class InheritMailTemplate(models.Model):
    _inherit = 'mail.template'

    not_send_ids = fields.Many2many('res.partner', string="Do Not Send")
