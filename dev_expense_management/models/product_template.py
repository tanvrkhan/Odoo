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

class product_template(models.Model):
    _inherit = 'product.template'
    
    misc_expense = fields.Boolean('Can Be Misc Expense')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: