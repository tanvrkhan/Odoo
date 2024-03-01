# Copyright 2018 ForgeFlow (https://www.forgeflow.com)
# @author Jordi Ballester <jordi.ballester@forgeflow.com.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def match_invoice(self):
        for rec in self:
            if rec.state=='posted':
                if rec.move_type=='in_invoice':
                    if rec.payment_state=='not_paid' or rec.payment_state=='partial':
                        matchingpayments = self.env['account.move'].search(['&','&','&',('payment_id.payment_type','=','outbound'),('partner_id','=',rec.partner_id.id),('company_id','=',rec.company_id.id),('amount_total_in_currency_signed','=',rec.amount_residual)],order='date desc', limit=1)
                        if matchingpayments:
                            for matchingpayment in matchingpayments:
                                total_payment_amount=matchingpayment.amount_total_in_currency_signed
                                payment_previous_matched_entries= self.env['account.partial.reconcile'].search([('debit_move_id', '=', matchingpayment.id)])
                                if payment_previous_matched_entries:
                                    for previous_matching in payment_previous_matched_entries:
                                        total_payment_amount-=previous_matching.amount
                                if total_payment_amount == rec.amount_residual:
                                    line1 = self.env['account.move.line'].search(
                                        [('move_id', '=', rec.id), ('account_id.account_type', '=', 'liability_payable')])
                                    lines = self.env['account.move.line'].browse(line1.id)
                                    lines += matchingpayment.line_ids.filtered(
                                        lambda line: line.account_id == lines[0].account_id and not line.reconciled)
                                    lines.reconcile()
                elif rec.move_type=='out_invoice':
                    if rec.payment_state=='not_paid' or rec.payment_state=='partial':
                        matchingpayments = self.env['account.move'].search(['&','&','&',('payment_id.payment_type','=','inbound'),('partner_id','=',rec.partner_id.id),('company_id','=',rec.company_id.id),('amount_total_in_currency_signed','=',rec.amount_residual)],order='date desc', limit=1)
                        if matchingpayments:
                            for matchingpayment in matchingpayments:
                                total_payment_amount=matchingpayment.amount_total_in_currency_signed
                                if matchingpayment:
                                    payment_previous_matched_entries = self.env['account.partial.reconcile'].search([('credit_move_id', '=', matchingpayment.id)])
                                    if payment_previous_matched_entries:
                                        for previous_matching in payment_previous_matched_entries:
                                            if previous_matching.debit_move_type=='out_invoice':
                                                total_payment_amount -= previous_matching.amount
                                    if total_payment_amount == rec.amount_residual:
                                        line1 = self.env['account.move.line'].search([('move_id','=',rec.id),('display_type','=','payment_term')])
                                        lines= self.env['account.move.line'].browse(line1.id)
                                        lines += matchingpayment.line_ids.filtered(lambda line: line.account_id == lines[0].account_id and not line.reconciled)
                                        lines.reconcile()
    # def reset_invoice(self):
    #     for rec in self:
    #         # query = """SELECT credit_move_id FROM account_partial_reconcile WHERE debit_move_id = %s"""
    #         # so_query = self._cr.execute(query, [self.id])
    #         # result = self._cr.fetchall()
    #         # if result:
    #
    #
    #         lines = rec._get_reconciled_amls()
    #
    #         lines = self.env['account.move.line'].search(
    #                 [('ids', '=', rec.id), ('display_type', '=', 'payment_term')])
    #         # payment= self.env['account.payment'].search([]).filtered(lambda p: rec.id in p.reconciled_invoice_ids.ids)
    #
    #         rec.button_draft()
    #         if lines:
    #             for line in lines:
    #                 line.remove_move_reconcile()
    #             # lines = self.env['account.move.line'].search([]).filtered(lambda p: payment.move_id in p.move_id and (p.account_id == rec.partner_id.property_account_payable_id or p.account_id  == rec.partner_id.property_account_receivable_id)) \
    #                 # ('ids','in',payment.move_id.line_ids)
    #         # lines= self.env['account.move'].search('id','in',payment_ids)
    #             rec._post()
    #             lines += self.env['account.move.line'].search(
    #                 [('move_id', '=', rec.id), ('display_type', '=', 'payment_term')])
    #             # lines += invoice_payment_line
    #             if not rec.has_reconciled_entries:
    #                 lines.reconcile()
    #         else:
    #             rec._post()
            # rec.payment_ids= [(6,0,payment_ids)]
            
                                
                                # self.env['account.partial.reconcile'].create({
                                #         'debit_move_id':rec.id,
                                #         'credit_move_id':matchingpayment.id,
                                #         'debit_amount_currency':rec.amount_residual,
                                #         'credit_amount_currency':rec.amount_residual,
                                #         'amount':round(rec.currency_id._convert(
                                #     rec.amount_residual,
                                #     rec.company_id.currency_id, rec.company_id, rec.date, True),2)
                                #
                                #     })
                                # rec.payment_state='paid'
                            
                        
