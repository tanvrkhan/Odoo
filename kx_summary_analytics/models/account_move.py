# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import base64
from operator import itemgetter

class AccountMove(models.Model):
    _inherit = "account.move"
    analytic_accounts_summary = fields.Char(string='Analytic Accounts', compute='_summarize_analytics')
    def _summarize_analytics(self):
        for invoice in self:
            analytic_account_names = ''
            if invoice.invoice_line_ids:
                for line in invoice.invoice_line_ids:
                    if line.analytic_distribution:
                        analytic_account_keys = line.analytic_distribution.keys()
                        if analytic_account_keys:
                            analytic_value=''
                            for key in analytic_account_keys:
                                analytic_name = self.env['account.analytic.account'].search([('id', '=', key),])
                                for entry in analytic_name:
                                    if analytic_name:
                                        analytic_account_names=entry.name+', '+analytic_account_names
                    else:
                        invoice.analytic_accounts_summary = ''
                invoice.analytic_accounts_summary = analytic_account_names
            else:
                invoice.analytic_accounts_summary = ''


