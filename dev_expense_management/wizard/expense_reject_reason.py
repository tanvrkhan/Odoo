# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _


class dev_expense_reject_reason(models.TransientModel):
    _name = "dev.expense.reject.reason"
    _description="Expense Reject Reason"
    
    
    reason = fields.Text('Reason', required="1")
    
    def reject_expense_request(self):
        active_ids = self._context.get('active_ids')
        expense_ids = self.env['dev.expense'].browse(active_ids)
        for exp in expense_ids:
            exp.reject_reason = self.reason
            exp.reject_user_id = self.env.user.id
            exp.reject_expense()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
    
