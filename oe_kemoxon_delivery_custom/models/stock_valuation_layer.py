# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError, Warning


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    costed_quantity = fields.Float()
    
    def update_quantity_from_delivery(self):
        for record in self:
            if record.stock_move_id:
                if record.quantity < 0:
                    record.quantity = record.stock_move_id.quantity_done * -1
                    self.update_valuation(record.unit_cost, record)
    
    def update_stock_value_to_match_initial_if_cancelled_out(self):
        for record in self:
            if record.stock_move_id.picking_id:
                if record.stock_move_id:
                    if record.stock_move_id.purchase_line_id:
                        cost = record.stock_move_id.purchase_line_id.price_unit / record.stock_move_id.purchase_line_id.order_id.currency_rate
                        self.update_valuation(cost, record)
                    # check if move is now 0
                    elif record.stock_move_id.quantity_done == 0:
                        all_value_layers = record.stock_move_id.stock_valuation_layer_ids
                        for valuation in all_value_layers:
                            if valuation.account_move_id:
                                for ae in valuation.account_move_id:
                                    if ae.has_reconciled_entries:
                                        break
                                    else:
                                        ae.state = 'draft'
                                        ae.line_ids.unlink()
                                        self.env['account.move'].search([('id', '=', ae.id)]).unlink()
                            valuation.unit_cost = 0
                            valuation.value = 0
                            valuation.quantity = 0
                    
                    else:
                        # get all valuations
                        earliest_valuation = self.env['stock.valuation.layer'].search(
                            ['&', ('stock_move_id', '=', record.stock_move_id.id),
                             ('product_id', '=', record.product_id.id)], order='id asc', limit=1)
                        cost_of_earliest_valuation = earliest_valuation.unit_cost
                        if record != earliest_valuation:
                            self.update_valuation(cost_of_earliest_valuation, record)
                        else:
                            all_purchases_before = self.env['stock.valuation.layer'].search(
                                ['&', '&', ('product_id', '=', record.product_id.id),
                                 ('stock_move_id', '!=', record.stock_move_id.id),
                                 ('stock_move_id.date', '<=', record.stock_move_id.date)])
                            if all_purchases_before:
                                total_quantity = 0
                                total_amount = 0
                                for purchase in all_purchases_before:
                                    total_amount += purchase.value
                                    total_quantity += purchase.quantity
                                avco = total_amount / total_quantity
                                self.update_valuation(avco, record)
                            else:
                                self.calculate_costing_from_later_dates(record)
    
    def update_valuation(self, cost, valuation):
        amount_to_post = cost * valuation.quantity
        valuation.unit_cost = amount_to_post / valuation.quantity
        valuation.value = amount_to_post
        accounting_header = valuation.account_move_id
        accounting_entries = valuation.account_move_id.line_ids
        for ae in accounting_entries:
            ae.remove_move_reconcile()
        amount_to_post = amount_to_post * -1 if amount_to_post < 0 else amount_to_post
        accounting_header.amount_untaxed = amount_to_post
        accounting_header.amount_total = amount_to_post
        accounting_header.amount_residual = amount_to_post
        accounting_header.amount_untaxed_signed = amount_to_post
        accounting_header.amount_total_signed = amount_to_post
        accounting_header.amount_total_in_currency_signed = amount_to_post
        accounting_header.amount_residual_signed = amount_to_post
        for ae in accounting_entries:
            ae.remove_move_reconcile()
            if ae.amount_currency != 0:
                if ae.amount_currency > 0:
                    ae.with_context(
                        check_move_validity=False).amount_currency = amount_to_post
                    ae.with_context(check_move_validity=False).debit = amount_to_post
                elif ae.amount_currency < 0:
                    ae.with_context(
                        check_move_validity=False).amount_currency = -1 * amount_to_post
                    ae.with_context(
                        check_move_validity=False).credit = amount_to_post
        accounting_header.state = 'posted'
    
    def remove_from_valuation(self):
        for record in self:
            if record.quantity == 0 or record.value == 0:
                record.delete_valuation(record)
            elif record.stock_move_id.picking_id:
                if record.stock_move_id.quantity_done == 0:
                    record.delete_valuation(record)
            else:
                record.delete_valuation(record)

    def delete_valuation(self,record):
            record.unit_cost = 0
            record.value = 0
            record.quantity = 0
            if record.account_move_id:
                for ae in record.account_move_id:
                    for ael in ae.line_ids:
                        ael.remove_move_reconcile()
                    ae.state = 'draft'
                    ae.line_ids.unlink()
                    self.env['account.move'].search([('id', '=', ae.id)]).unlink()
            self.env['stock.valuation.layer'].search([('id', '=', record.id)]).unlink()
    
    def update_date_to_schedule_date(self):
        for record in self:
            next_number = self.env['ir.sequence'].next_by_code('stock.valuation')
            next_number = str(next_number)
            # next_number = next_number[-5:]
            year = record.stock_move_id.picking_id.scheduled_date.year
            month = record.stock_move_id.picking_id.scheduled_date.month
            sequence = 'STJU/' + str(year) + '/' + str(month) + '/' + next_number
            
            for line in record.stock_move_id.move_line_ids:
                line.date = line.move_id.picking_id.scheduled_date
            record.create_date = record.stock_move_id.picking_id.scheduled_date
            record.stock_move_id.picking_id.date_done = record.stock_move_id.picking_id.scheduled_date
            record.stock_move_id.date = record.stock_move_id.picking_id.scheduled_date
            
            record.account_move_id.state = 'draft'
            record.account_move_line_id.parent_state = 'draft'
            record.account_move_id.name = 'draft'
            record.account_move_id.date = record.stock_move_id.picking_id.scheduled_date.date()
            record.account_move_id.name = sequence
            record.account_move_line_id.date = record.stock_move_id.picking_id.scheduled_date.date()
            record.account_move_id.state = 'posted'
            record.account_move_line_id.parent_state = 'posted'
        return self
    
    def recalculate_stock_value(self):
        selfupdated = self.update_date_to_schedule_date()
        wrong = 0
        # sorted = self.env['stock.valuation.layer'].search([('id', 'in', [self.id])],order="id desc")
        # sorted = self.search([],order="id asc")
        # sorted={}
        # for rec in self
        # orderingdate= date.min
        # sortedself= sorted(self,key=lambda x:x["create_date"],reverse=True)
        sortedself = self.sorted(key=lambda r: r.create_date)
        
        for record in sortedself:
            if record.stock_move_id.quantity_done == 0:
                for acce in record.account_move_id.line_ids:
                    acce.remove_move_reconcile()
                record.remove_from_valuation()
            else:
                all_valuations = self.env['stock.valuation.layer'].search(
                    ['&', '&', '&',
                     ('product_id', '=', record.product_id.id),
                     ('stock_move_id.date', '<=', record.stock_move_id.date),
                     ('id', '!=', record.id),
                     ('warehouse_id', '=', record.warehouse_id.id),
                     ('company_id', '=', record.company_id.id),
                     ('quantity', '>', 0)
                     ])
                totalquantity = 0
                totalamount = 0
                
                base_currency = record.company_id.currency_id
                applicablequantity=0
                applicableamount =0
                rate=0
                rateusd=0
                if record.quantity > 0:
                    applicablequantity = record.quantity
                    # porateusd2 = record.stock_move_id.purchase_line_id.order_id.currency_id.compute(
                    #     record.stock_move_id.purchase_line_id.price_unit, record.stock_move_id.purchase_line_id.currency_id)
                    rate=record.stock_move_id.purchase_line_id.price_unit
                    rateusd = record.stock_move_id.purchase_line_id.order_id.currency_id._convert(
                        record.stock_move_id.purchase_line_id.price_unit,
                        base_currency, record.company_id, record.stock_move_id.date, True)
                    applicableamount += (rateusd * record.quantity)
                else:
                    if all_valuations:
                        for valuation in all_valuations:
                            totalquantity += valuation.quantity
                            totalamount += valuation.value
                    applicablequantity=record.quantity
                    rateusd=round(totalamount/totalquantity,2)
                    applicableamount = applicablequantity * rateusd
                    
                if applicablequantity!=0 and applicableamount!=0:
                    if round(record.unit_cost,2)!=round(rateusd,2):
                        wrong+= 1
                    record.unit_cost = rateusd
                    record.value = applicableamount
                    record.account_move_id.state = 'draft'
                    for ae in record.account_move_id.line_ids:
                        ae.remove_move_reconcile()
                        if ae.amount_currency != 0:
                            if ae.amount_currency > 0:
                                if record.quantity < 0:
                                    newquantity = record.quantity * -1
                                else:
                                    newquantity = record.quantity
                                ae.with_context(
                                    check_move_validity=False).amount_currency = rate * newquantity
                                ae.with_context(
                                    check_move_validity=False).debit = rateusd * newquantity
                            elif ae.amount_currency < 0:
                                if record.quantity > 0:
                                    newquantity = record.quantity * -1
                                else:
                                    newquantity = record.quantity
                                ae.with_context(
                                    check_move_validity=False).amount_currency = rate * newquantity
                                ae.with_context(
                                    check_move_validity=False).credit = rateusd* newquantity * -1
                    record.account_move_id.state = 'posted'
        if wrong > 0:
            self.recalculate_stock_value()
    
    # def recalculate_stock_value(self):
    #     for record in self:
    #         all_valuations = self.env['stock.valuation.layer'].search(
    #             ['&', '&', ('product_id', '=', record.product_id.id), ('stock_move_id', '!=', record.stock_move_id.id),
    #              ('stock_move_id.date', '<', record.stock_move_id.date)])
    #         remaining_quantity = record.quantity
    #         accumulated_quantity = 0
    #         amount2 = 0
    #         quantity2 = record.quantity
    #         for valuation in all_valuations:
    #             if valuation.quantity - valuation.costed_quantity > 0:
    #                 qty_to_cost=valuation.quantity - valuation.costed_quantity
    #                 remaining_quantity += qty_to_cost
    #                 if remaining_quantity <= 0 and qty_to_cost>0.00:
    #                     quantity2 += qty_to_cost
    #                     amount2 += valuation.value/valuation.quantity*qty_to_cost
    #                     accumulated_quantity += qty_to_cost
    #                     valuation.costed_quantity += qty_to_cost
    #                     if (remaining_quantity == 0):
    #                         break
    #                 else:
    #                     quantity2 = (valuation.quantity - remaining_quantity)
    #                     valuation.costed_quantity = quantity2
    #                     amount2 += quantity2 * valuation.unit_cost
    #                     break
    #         record.unit_cost = amount2 / (record.quantity * -1)
    #         record.value = record.quantity * record.unit_cost
    #         record.account_move_id.state = 'draft'
    #         for ae in record.account_move_id.line_ids:
    #             if ae.amount_currency != 0:
    #                 if ae.amount_currency > 0:
    #                     ae.with_context(
    #                         check_move_validity=False).amount_currency = record.unit_cost * record.quantity
    #                     ae.with_context(
    #                         check_move_validity=False).debit = record.unit_cost * record.quantity
    #                 elif ae.amount_currency < 0:
    #                     ae.with_context(
    #                         check_move_validity=False).amount_currency = -1 * record.unit_cost * record.quantity
    #                     ae.with_context(
    #                         check_move_validity=False).credit = record.unit_cost * record.quantity
    #         record.account_move_id.state = 'posted'
    # for record in self:
    #     if(record.quantity<0):
    #         total_amount=0.00
    #         total_quantity=0.00
    #         all_valuations_amounts=self.env['stock.valuation.layer'].search(['&','&',('product_id','=',record.product_id.id),('stock_move_id','!=',record.stock_move_id.id),('record.stock_move_id.date','<',record.stock_move_id.date)])
    #         if all_valuations_amounts:
    #             for valuation in all_valuations_amounts:
    #                 if(valuation.quantity>0):
    #                     total_quantity+=valuation.quantity
    #                     total_amount+=valuation.value
    #             if(total_quantity<=0):
    #                 self.calculate_costing_from_later_dates(record)
    #             else:
    #                 unit_cost=total_amount/total_quantity
    #                 record.unit_cost = unit_cost
    #                 record.value = record.quantity*record.unit_cost
    #                 record.account_move_id.state = 'draft'
    #                 for ae in record.account_move_id.line_ids:
    #                     if ae.amount_currency != 0:
    #                         if ae.amount_currency > 0:
    #                             ae.with_context(
    #                                 check_move_validity=False).amount_currency = valuation.unit_cost * valuation.quantity
    #                             ae.with_context(check_move_validity=False).debit = valuation.unit_cost * valuation.quantity
    #                         elif ae.amount_currency < 0:
    #                             ae.with_context(
    #                                 check_move_validity=False).amount_currency = -1 * valuation.unit_cost * valuation.quantity
    #                             ae.with_context(check_move_validity=False).credit = valuation.unit_cost * valuation.quantity
    #                 record.account_move_id.state = 'posted'
    #         else:
    #             self.calculate_costing_from_later_dates(record)
    #
    #
    #     else:
    #         if(record.stock_move_id.purchase_line_id):
    #             record.unit_cost=record.stock_move_id.purchase_line_id.price_unit
    #             record.value = record.quantity * record.unit_cost
    #             record.account_move_id.state = 'draft'
    #             for ae in record.account_move_id.line_ids:
    #                 if ae.amount_currency != 0:
    #                     if ae.amount_currency > 0:
    #                         ae.with_context(
    #                             check_move_validity=False).amount_currency = record.unit_cost * record.quantity
    #                         ae.with_context(
    #                             check_move_validity=False).debit = record.unit_cost * record.quantity
    #                     elif ae.amount_currency < 0:
    #                         ae.with_context(
    #                             check_move_validity=False).amount_currency = -1 * record.unit_cost * record.quantity
    #                         ae.with_context(
    #                             check_move_validity=False).credit = record.unit_cost * record.quantity
    #             record.account_move_id.state = 'posted'
    #
    
    def calculate_costing_from_later_dates(self, record):
        all_valuations_after = self.env['stock.valuation.layer'].search(
            ['&', '&', ('product_id', '=', record.product_id.id), ('stock_move_id', '!=', record.stock_move_id.id),
             ('stock_move_id.date', '>=', record.stock_move_id.date)])
        total_quantity = 0
        total_amount = 0
        for later_valuation in all_valuations_after:
            if (later_valuation.quantity > 0):
                total_amount += later_valuation.value
                total_quantity += later_valuation.quantity
        if total_amount and total_quantity:
            avco = total_amount / total_quantity
            self.update_valuation(avco, record)