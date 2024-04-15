# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    exp_payment_journal = fields.Many2one(related="company_id.exp_payment_journal", string="Payment Method", readonly=False)
    exp_journal_id = fields.Many2one(related="company_id.exp_journal_id", string="Expense Journal", readonly=False)
    exp_approval_amount = fields.Float(related="company_id.exp_approval_amount", string='Approval Amount', readonly=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: