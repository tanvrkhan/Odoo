# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date, formatLang


class InheritAccountPayment(models.Model):
    _inherit = 'account.payment'
    contraBankAmount = fields.Float("Contra amount")
    contraBankCurrency = fields.Many2one('res.currency', related="destination_journal_id.currency_id")
    def _create_paired_internal_transfer_payment(self):
        ''' When an internal transfer is posted, a paired payment is created
        with opposite payment_type and swapped journal_id & destination_journal_id.
        Both payments liquidity transfer lines are then reconciled..
        '''
        for payment in self:
            paired_payment = payment.copy({
                'journal_id': payment.destination_journal_id.id,
                'destination_journal_id': payment.journal_id.id,
                'payment_type': payment.payment_type == 'outbound' and 'inbound' or 'outbound',
                'move_id': None,
                'ref': payment.ref,
                'paired_internal_transfer_payment_id': payment.id,
                'date': payment.date,
             
            })
            paired_payment.move_id._post(soft=False)
            payment.paired_internal_transfer_payment_id = paired_payment

            body = _(
                "This payment has been created from %s",
                payment._get_html_link(),
            )
            paired_payment.message_post(body=body)
            body = _(
                "A second payment has been created: %s",
                paired_payment._get_html_link(),
            )
            payment.message_post(body=body)

            lines = (payment.move_id.line_ids + paired_payment.move_id.line_ids).filtered(
                lambda l: l.account_id == payment.destination_account_id and not l.reconciled)

            # to assign sequence make this as draft again
            paired_payment.sudo().action_draft()

            # again post it
            paired_payment.sudo().action_post()

            # custom logic starts here
            move_obj = self.env['account.move.line']
            
            payment_currency = payment.journal_id.currency_id or payment.env.company.currency_id
            paired_currency = paired_payment.journal_id.currency_id or payment.env.company.currency_id
            
            
            origin_amount=payment.amount
            destination_amount=payment.contraBankAmount
            if(payment_currency.id==2):
                convertedamount=origin_amount
            elif(paired_currency.id==2):
                convertedamount=destination_amount
             
            else:
                convertedamount=payment.amount * payment_currency.rate
            
            
            
            # paired_amount = move_obj.browse(paired_payment.line_ids.ids[0]).balance * paired_currency.rate
            # paired_amount_2 = move_obj.browse(paired_payment.line_ids.ids[1]).balance * paired_currency.rate
            paired_payment.move_id.line_ids = [
                (1, paired_payment.line_ids.ids[0], {'amount_currency': payment.contraBankAmount,
                                                     'currency_id': paired_currency,
                                                     'balance':convertedamount}),
                (1, paired_payment.line_ids.ids[1], {'amount_currency': payment.contraBankAmount*-1,
                                                     'currency_id': paired_currency,
                                                     'balance':convertedamount*-1})
            ]
            payment.move_id.line_ids = [
                (1, payment.line_ids.ids[0], {'amount_currency': payment.amount,
                                              'currency_id': payment_currency,
                                              'balance':convertedamount}),
                (1, payment.line_ids.ids[1], {'amount_currency': payment.amount*-1,
                                              'currency_id': payment_currency,
                                               'balance':convertedamount*-1})
            ]
            
            

            # paired_payment.move_id.line_ids = [
            #     (1, paired_payment.line_ids.ids[0], {'amount_currency': paired_amount,
            #                                          'currency_id': paired_currency}),
            #     (1, paired_payment.line_ids.ids[1], {'amount_currency': paired_amount_2,
            #                                          'currency_id': paired_currency})
            # ]
            #
            # # inter payment which we create
            #
            #
            # payment_amount = move_obj.browse(payment.line_ids.ids[0]).balance * payment_currency.rate
            # payment_amount_2 = move_obj.browse(payment.line_ids.ids[1]).balance * payment_currency.rate

           

            lines.reconcile()

    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):

            # After the migration to 14.0, the journal entry could be shared between the account.payment and the
            # account.bank.statement.line. In that case, the synchronization will only be made with the statement line.
            if pay.move_id.statement_line_id:
                continue

            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}

            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(_("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

                if len(liquidity_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one outstanding payments/receipts account.",
                        move.display_name,
                    ))

                if len(counterpart_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one receivable/payable account (with an exception of "
                        "internal transfers).",
                        move.display_name,
                    ))

                # if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                #     raise UserError(_(
                #         "Journal Entry %s is not valid. In order to proceed, the journal items must "
                #         "share the same currency.",
                #         move.display_name,
                #     ))

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same partner.",
                        move.display_name,
                    ))

                if counterpart_lines.account_id.account_type == 'asset_receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency

                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    'amount': abs(liquidity_amount),
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                if liquidity_amount > 0.0:
                    payment_vals_to_write.update({'payment_type': 'inbound'})
                elif liquidity_amount < 0.0:
                    payment_vals_to_write.update({'payment_type': 'outbound'})

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))
