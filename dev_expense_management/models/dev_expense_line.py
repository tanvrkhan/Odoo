# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models, fields, api, _


class dev_expense_line(models.Model):
    _name = 'dev.expense.line'
    _description = "Expense Lines"
    
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char('Description', required="1")
    account_id = fields.Many2one('account.account', string='Account')
    quantity = fields.Float('Quantity', default=1, required="1")
    unit_price = fields.Float('Unit Price', required="1")
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    expense_id = fields.Many2one('dev.expense', string='Expense')
    currency_id = fields.Many2one("res.currency", string='Currency')
    amount_total = fields.Monetary('Total', compute='get_total_amount', currency_field = 'currency_id')
    attachment_id = fields.Many2many('ir.attachment', string="Bill Attachment")
 
    @api.depends('quantity','unit_price','tax_ids')
    def get_total_amount(self):
        for line in self:
            line.amount_total = line.unit_price * line.quantity
            
    @api.onchange('product_id')
    def onchange_product_id(self):
        account_id = False
        if self.product_id and self.product_id.property_account_expense_id:
            account_id = self.product_id.property_account_expense_id.id
        if not account_id:
            if self.product_id.categ_id and self.product_id.categ_id.property_account_expense_categ_id:
                account_id = self.product_id.categ_id.property_account_expense_categ_id.id
        if self.product_id:
            self.name = self.product_id.display_name
            self.quantity = 1
            self.unit_price = self.product_id.list_price
            self.account_id = account_id

# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:
