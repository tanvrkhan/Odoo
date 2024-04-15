# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, models


class ExpenseManagementReport(models.AbstractModel):
    _name = 'report.dev_expense_management.exp_report_template'
    _description = "Expense Report"

    def _get_report_values(self, docids, data=None):
        docs = self.env['dev.expense'].browse(docids)
        return {'doc_ids': docids,
                'doc_model': 'dev.expense',
                'docs': docs,
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
