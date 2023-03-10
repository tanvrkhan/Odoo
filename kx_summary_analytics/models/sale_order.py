# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class SaleOrder(models.Model):
    _inherit = "sale.order"
    analytic_accounts_summary = fields.Char(string='Analytic Accounts', compute='_summarize_analytics')
    def _summarize_analytics(self):
        for order in self:
            analytic_account_names = ''
            if order.order_line:
                for line in order.order_line:
                    if line.analytic_distribution:
                        analytic_account_keys = line.analytic_distribution.keys()
                        if analytic_account_keys:
                            analytic_value = ''
                            for key in analytic_account_keys:
                                analytic_name = self.env['account.analytic.account'].search([('id', '=', key), ])
                                for entry in analytic_name:
                                    if analytic_name:
                                        analytic_account_names = entry.name + ', ' + analytic_account_names
                    else:
                        order.analytic_accounts_summary = ''
                order.analytic_accounts_summary = analytic_account_names
            else:
                order.analytic_accounts_summary = ''

