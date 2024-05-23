# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError, Warning
from datetime import datetime, timedelta


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
                record.delete_valuation()
            elif record.stock_move_id.picking_id:
                if record.stock_move_id.quantity_done == 0:
                    record.delete_valuation()
            else:
                record.delete_valuation()

    def delete_valuation(self):
        for rec in self:
            rec.unit_cost = 0
            rec.value = 0
            rec.quantity = 0
            if rec.account_move_id:
                for ae in rec.account_move_id:
                    for ael in ae.line_ids:
                        ael.remove_move_reconcile()
                    ae.state = 'draft'
                    ae.line_ids.unlink()
                    self.env['account.move'].search([('id', '=', ae.id)]).unlink()
            self.env['stock.valuation.layer'].search([('id', '=', rec.id)]).unlink()
    def delete_valuation_force(self):
        for rec in self:
            rec.unit_cost = 0
            rec.value = 0
            rec.quantity = 0
            if rec.account_move_id:
                for ae in rec.account_move_id:
                    for ael in ae.line_ids:
                        ael.remove_move_reconcile()
                    ae.state = 'draft'
                    ae.line_ids.unlink()
                    self.env['account.move'].search([('id', '=', ae.id)]).unlink()
            if rec.stock_move_id:
                if rec.stock_move_id.picking_id:
                    self.env['stock.picking'].search([('stock_move_id', '=', rec.stock_move_id.picking_id.id)]).set_stock_move_to_draft()
                else:
                    self.env['stock.move.line'].search(
                        [('move_id', '=', rec.stock_move_id.id)]).state='draft'
                    self.env['stock.move.line'].search(
                        [('move_id', '=', rec.stock_move_id.id)]).unlink()
                    self.env['stock.move'].search(
                        [('id', '=', rec.stock_move_id.id)]).state='draft'
                    self.env['stock.move'].search(
                        [('id', '=', rec.stock_move_id.id)]).unlink()
            self.env['stock.valuation.layer'].search([('id', '=', rec.id)]).unlink()
            #     self.env['stock.move'].search([('id', '=', rec.stock_move_id)]).unlink()
            # self.env['stock.valuation.layer'].search([('id', '=', rec.id)]).unlink()
    def update_date_to_schedule_date(self):
        for record in self:
            next_number = self.env['ir.sequence'].next_by_code('stock.valuation')
            next_number = str(next_number)
            if record.stock_move_id.picking_id.custom_delivery_date:
                datetocheck=record.stock_move_id.picking_id.custom_delivery_date
            else:
                datetocheck=record.stock_move_id.picking_id.scheduled_date
            datetouse=datetocheck
            if datetouse:
                datetouse=self.verify_picking_date(record,datetocheck)
                
                
                # next_number = next_number[-5:]
                year = datetouse.year
                month = datetouse.month
                sequence = 'STJU/' + str(year) + '/' + str(month) + '/' + next_number
                
                for line in record.stock_move_id.move_line_ids:
                    line.date = datetouse
                record.create_date = datetouse
                record.stock_move_id.picking_id.date_done = datetouse
                record.stock_move_id.date = datetouse
                
                self.reset_accounting(record)
        return self
    def verify_picking_date(self, record,datetocheck):
        result=datetime.combine(datetocheck, datetime.min.time())
        if record.quantity>0:
            interval =-5
        else:
            interval = 5
        while record.check_if_exists(record,result):
            result = result + timedelta(minutes=interval)
            # record.verify_picking_date( record, result)
        return result
    def check_if_exists(self,record,datetocheck):
        all_pickings = record.env['stock.picking'].search(
            ['&', '&',
            ('date_done', '=', datetocheck),
            ('id', '!=', record.stock_move_id.picking_id.id),
            ('company_id', '=', record.company_id.id)
            ])
        if all_pickings:
            return True
        else:
            return False
    
    def update_date_without_accounting_date(self):
        for record in self:
            next_number = self.env['ir.sequence'].next_by_code('stock.valuation')
            next_number = str(next_number)
            if record.stock_move_id.picking_id.custom_delivery_date:
                datetocheck = record.stock_move_id.picking_id.custom_delivery_date
            else:
                datetocheck = record.stock_move_id.picking_id.scheduled_date
            datetouse = datetocheck
            if datetouse:
                datetouse = self.verify_picking_date(record, datetocheck)
                
                # next_number = next_number[-5:]
                year = datetouse.year
                month = datetouse.month
                sequence = 'STJU/' + str(year) + '/' + str(month) + '/' + next_number
                
                for line in record.stock_move_id.move_line_ids:
                    line.date = datetouse
                record.create_date = datetouse
                record.stock_move_id.picking_id.date_done = datetouse
                record.stock_move_id.date = datetouse
                
                # self.reset_accounting(record)
        return self
    
    def recalculate_stock_value(self):
        self.update_date_without_accounting_date()
        self.env.cr.commit()
        wrong = 0
        sortedself = self.sorted(key=lambda r: r.create_date)
        stock_valuations = self.env['stock.valuation.layer'].search([])
        
        for record in sortedself:
            sm = record.stock_move_id
            picking = record.stock_move_id.picking_id
            am = record.account_move_id
            aml = record.account_move_id.line_ids
            
            applicablequantity = 0
            applicableamount = 0
            if sm.quantity_done == 0:
                aml.remove_move_reconcile()
                am.button_draft()
                am.button_cancel()
                record.remove_from_valuation()
                continue
            elif picking.valuation_price != 0:
                record.unit_cost = picking.valuation_price
                record.value = record.quantity * picking.valuation_price
                self.reset_accounting(record)
                return
            #purchase transaction
            elif record.quantity > 0:
                #internal transfer
                if sm.location_id.usage == 'internal' and sm.location_dest_id.usage == 'internal':
                    all_valuations = stock_valuations.search(
                    [
                        ('stock_move_id', '=', sm.id),
                        ('quantity', '=', record.quantity * -1)
                    ])
                    total_quantity = sum(v.quantity for v in all_valuations)
                    total_value = sum(v.value for v in all_valuations)
                    applicablequantity = record.quantity
                    temprate = total_value / total_quantity
                    applicableamount = applicablequantity * temprate
                #external purchase
                else:
                    pl= sm.purchase_line_id
                    base_currency = record.company_id.currency_id
                    applicablequantity = record.quantity
                    rate=round(pl.price_unit,2)
                    rateusd = round(pl.order_id.currency_id._convert(
                        pl.price_unit,
                        base_currency, record.company_id, sm.date, True),2)
                    applicableamount += (rateusd * record.quantity)
            #sales transaction
            elif record.quantity < 0:
                domain = [
                    ('product_id', '=', record.product_id.id),
                    ('stock_move_id.date', '<=', record.stock_move_id.date),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id)
                ]
                domain.append(('warehouse_id', '=', record.warehouse_id.id))
                all_valuations = stock_valuations.search(domain)
                if all_valuations:
                    total_quantity = sum(v.quantity for v in all_valuations)
                    total_value = sum(v.value for v in all_valuations)
                    if total_quantity<0:
                        raise ValidationError("Quantity in the warehouse is not enough for this transaction.")
                    
                    else:
                        rateusd = round(total_value/total_quantity, 2)
                        applicablequantity = record.quantity
                        applicableamount = applicablequantity * rateusd
            #force feeding rate if valuation price is not 0
            
            if applicablequantity!=0 and applicableamount!=0:
                rateusd = round(applicableamount / applicablequantity, 2)
                if round(record.unit_cost,2)!=round(rateusd,2):
                    wrong+= 1
                record.unit_cost = rateusd
                record.value = applicableamount
                self.reset_accounting(record)
    
        if wrong > 0:
            self.recalculate_stock_value()
                
                
    def reset_accounting(self,record):
        record.account_move_id.line_ids.remove_move_reconcile()
        record.account_move_id.button_draft()
        record.account_move_id.button_cancel()
        record._validate_accounting_entries()
                    # record.account_move_id.state = 'draft'
                    # for ae in record.account_move_id.line_ids:
                    #     ae.remove_move_reconcile()
                    #     if ae.amount_currency != 0:
                    #         if ae.amount_currency > 0:
                    #             if record.quantity < 0:
                    #                 newquantity = record.quantity * -1
                    #             else:
                    #                 newquantity = record.quantity
                    #             ae.with_context(
                    #                 check_move_validity=False).amount_currency = rate * newquantity
                    #             ae.with_context(
                    #                 check_move_validity=False).debit = rateusd * newquantity
                    #         elif ae.amount_currency < 0:
                    #             if record.quantity > 0:
                    #                 newquantity = record.quantity * -1
                    #             else:
                    #                 newquantity = record.quantity
                    #             ae.with_context(
                    #                 check_move_validity=False).amount_currency = rate * newquantity
                    #             ae.with_context(
                    #                 check_move_validity=False).credit = rateusd* newquantity * -1
                    # record.account_move_id.state = 'posted'

    
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