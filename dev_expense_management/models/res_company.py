# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, exceptions, _

class res_company(models.Model):
    _inherit = 'res.company'
    
    exp_payment_journal = fields.Many2one('account.journal', string="Payment Method")
    exp_journal_id = fields.Many2one('account.journal', string="Expense Journal")
    exp_approval_amount = fields.Float('Approval Amount')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: