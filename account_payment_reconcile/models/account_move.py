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
                            
                        
