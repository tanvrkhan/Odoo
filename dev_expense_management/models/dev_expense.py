# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang
from odoo import models, fields, api, _


class dev_expense(models.Model):
    _name = 'dev.expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'
    _description = 'Manage Expense'

    def get_currency(self):
        company_id = self.env.user.company_id
        return company_id.currency_id.id

    def get_account_id_from_journal(self):
        journal = self.journal_id
        account_id = journal.company_id.account_journal_payment_credit_account_id
        return account_id

    def _prepare_move_values(self):
        account_date = self.date
        move_values = {
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'date': account_date,
            'ref': self.name,
            'name': '/',
            'move_type': 'entry'
        }
        return move_values

    def get_tax_account(self):
        biggest_tax_id = False
        biggest_tax_amount = 0
        tax_account_id = False
        for line in self.expense_lines:
            if line.tax_ids:
                for tax_id in line.tax_ids:
                    if tax_id.amount > biggest_tax_amount:
                        biggest_tax_amount = tax_id.amount
                        biggest_tax_id = tax_id
        if not biggest_tax_id.invoice_repartition_line_ids:
            raise ValidationError(_('''Account for tax is not found, Please configure 'Distribution for Invoices' into '%s' tax. Add one line 'Based on Tax' also add valid account on that line''') % (biggest_tax_id.name))
        if biggest_tax_id and biggest_tax_id.invoice_repartition_line_ids:
            for line in biggest_tax_id.invoice_repartition_line_ids:
                if line.repartition_type == 'tax' and line.account_id:
                    tax_account_id = line.account_id
                    break
        if not tax_account_id:
            raise ValidationError(_('''Account for tax is not found, Please configure 'Distribution for Invoices' into '%s' tax. Add one line 'Based on Tax' also add valid account on that line''') % (biggest_tax_id.name))
        return tax_account_id

    def _prepare_move_line_values(self):
        tax_account_id = False
        if self.amount_tax:
            tax_account_id = self.get_tax_account()
        move_lines = []
        # source line
        company_currency = self.company_id.currency_id
        for expense_line in self.expense_lines:
            currency_converted_amount = self.currency_id._convert(expense_line.amount_total,
                                                                  company_currency,
                                                                  self.company_id,
                                                                  self.date)
            move_line_src = {
                'name': expense_line.product_id and expense_line.product_id.name or '/',
                'quantity': expense_line.quantity,
                'debit': currency_converted_amount,
                'credit': 0,
                'amount_currency': expense_line.amount_total,
                'account_id': expense_line.account_id and expense_line.account_id.id or False,
                'product_id': expense_line.product_id and expense_line.product_id.id or False,
                'product_uom_id': expense_line.product_id and expense_line.product_id.uom_id and expense_line.product_id.uom_id.id or False,
                'currency_id': expense_line.currency_id and expense_line.currency_id.id or False,
            }
            move_lines.append(move_line_src)
        if self.amount_tax > 0:
            currency_converted_amount = self.currency_id._convert(self.amount_tax,
                                                                  company_currency,
                                                                  self.company_id,
                                                                  self.date)
            move_line_src = {
                'name': 'Tax',
                'debit': currency_converted_amount,
                'credit': 0,
                'amount_currency': self.amount_tax,
                'account_id': tax_account_id and tax_account_id.id or False,
                'currency_id': self.currency_id and self.currency_id.id or False,
            }
            move_lines.append(move_line_src)

        # destination line
        currency_converted_amount = self.currency_id._convert(self.amount_total,
                                                              company_currency,
                                                              self.company_id,
                                                              self.date)
        account_id = self.get_account_id_from_journal()
        move_line_dst = {
            'name': self.name,
            'debit': 0,
            'credit': currency_converted_amount,
            'amount_currency': -currency_converted_amount,
            'account_id': account_id and account_id.id or False,
            'date_maturity': self.date,
            'currency_id': self.currency_id and self.currency_id.id or False,
        }
        move_lines.append(move_line_dst)
        return move_lines

    def create_expense_journal_entry(self):
        move_vals = self._prepare_move_values()
        move_id = self.env['account.move'].with_context(default_journal_id=self.journal_id.id).create(move_vals)
        move_line_values = self._prepare_move_line_values()
        move_id.write({'line_ids': [(0, 0, line) for line in move_line_values]})
        if move_id:
            self.move_id = move_id.id

    @api.depends('expense_lines.amount_total')
    def _compute_amount(self):
        for expense in self:
            tax_rounding_method = expense.company_id.tax_calculation_rounding_method
            expense.amount_untaxed = sum(line.amount_total for line in self.expense_lines)
            tax_amount = 0
            tax_lines_vals_merged = {}
            for line in expense.expense_lines:
                tax_info = line.tax_ids.compute_all(line.unit_price, expense.currency_id, line.quantity, line.product_id, False)
                if tax_rounding_method == 'round_globally':
                    for t in tax_info.get('taxes', False):
                        key = (
                            t['id'],
                            t['account_id'],
                        )
                        if key not in tax_lines_vals_merged:
                            tax_lines_vals_merged[key] = t.get('amount', 0.0)
                        else:
                            tax_lines_vals_merged[key] += t.get('amount', 0.0)
                else:
                    tax_amount += sum([t.get('amount', 0.0) for t in tax_info.get('taxes', False)])

            if tax_rounding_method == 'round_globally':
                tax_amount = sum([expense.currency_id.round(t) for t in tax_lines_vals_merged.values()])

            expense.amount_tax = tax_amount
            expense.amount_total = expense.amount_untaxed + expense.amount_tax

    @api.model
    def create(self, vals):
        vals.update({
            'name': self.env['ir.sequence'].next_by_code('dev.expense') or '/'
        })
        return super(dev_expense, self).create(vals)

    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(dev_expense, self).copy(default=default)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            self.journal_id = self.company_id.exp_journal_id and self.company_id.exp_journal_id.id or False
            self.payment_journal_id = self.company_id.exp_payment_journal and self.company_id.exp_payment_journal.id or False
            self.currency_id = self.company_id.currency_id and self.company_id.currency_id.id or False
        else:
            self.journal_id = self.payment_journal_id = self.currency_id = False

    def unlink(self):
        for expense in self:
            if expense.state not in ('draft', 'cancel'):
                raise ValidationError(_('You can not delete a Expense. You must first cancel it.'))
        return super(dev_expense, self).unlink()

    def button_journal_entries(self):
        action = self.env.ref('account.action_move_journal_line').read()[0]
        if action:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = self.move_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


    def send_approval_mail(self):
        group_id = self.env.ref('account.group_account_manager')
        company_email = self.company_id and self.company_id.email or ''
        if not company_email:
            company_email = self.env.company and self.env.company.email or ''
        if company_email:
            if group_id and group_id.users:
                template_id = self.env.ref('dev_expense_management.dev_expense_account_manager_mail_template')
                if template_id:
                    for user in group_id.users:
                        if user.partner_id and user.partner_id.email:
                            template_id.write({'email_to': user.partner_id.email,
                                               'email_from': self.company_id.email})
                            template_id.send_mail(self.id, True)

    def send_request(self):
        self.state = 'approve'
        if self.env.user.has_group('account.group_account_manager'):
            self.done_expense()
        else:
            if self.company_id.exp_approval_amount <= self.amount_total:
                self.send_approval_mail()
                self.state = 'approve'
            else:
                self.done_expense()

    def done_expense(self):
        self.create_expense_journal_entry()
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def reject_expense(self):
        self.state = 'reject'
        template_id = self.env.ref('dev_expense_management.dev_expense_reject_mail_template')
        email_from = self.env.user and self.env.user.partner_id and self.env.user.partner_id.email or ''
        email_to =  self.user_id and self.user_id.partner_id and self.user_id.partner_id.email or ''
        if template_id and email_from and email_to:
            template_id.write({'email_to': email_to,
                               'email_from': email_from})
            template_id.send_mail(self.id, True)

    def cancel_expense(self):
        self.state = 'cancel'

    def get_expense_detail(self):
        line_data = []
        for line in self.expense_lines:
            line_dict = {'name': line.name or '',
                         'quantity': line.quantity,
                         'price': line.unit_price,
                         'total': line.amount_total}
            line_data.append(line_dict)
        return line_data

    name = fields.Char('Name', required="1", default='/')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, required="1")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly="1")
    date = fields.Date('Bill Date', default=fields.Date.today(), copy=False, required=True)
    journal_id = fields.Many2one('account.journal', string='Expense Journal', required="1")
    payment_journal_id = fields.Many2one('account.journal', string='Payment Method', required="1")
    currency_id = fields.Many2one('res.currency', string='Currency', default=get_currency, required="1")
    memo = fields.Char('Memo')
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approve'), ('done', 'Done'), ('reject', 'Reject'), ('cancel', 'Cancel')], default='draft')
    note = fields.Text('Internal Notes')
    expense_lines = fields.One2many('dev.expense.line', 'expense_id', string='Expense Lines')
    product_id = fields.Many2one('product.product', related='expense_lines.product_id', string='Product')
    move_id = fields.Many2one('account.move', 'Journal Entry', copy=False)
    reject_user_id = fields.Many2one('res.users', copy=False)
    reject_reason = fields.Text('Reject Reason')
    amount_untaxed = fields.Monetary(string='Untaxed Amount',
                                     store=True, readonly=True, compute='_compute_amount')
    amount_tax = fields.Monetary(string='Tax',
                                 store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Monetary(string='Total',
                                   store=True, readonly=True, compute='_compute_amount')
    submitted_by = fields.Many2one('hr.employee', string='Submitted By')

# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:
