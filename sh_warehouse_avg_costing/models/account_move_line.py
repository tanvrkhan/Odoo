# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models

class WarehouseAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # def _stock_account_get_anglo_saxon_price_unit(self):
    #     # * Softhealer code Start *
    #
    #     #  Passed the warehouse id in _stock_account_get_anglo_saxon_price_unit
    #
    #     # * Softhealer code end *
    #     self.ensure_one()
    #     warehouse = False
    #     query = """SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id = %s"""
    #     so_query = self._cr.execute(query, [self.id])
    #     result = self._cr.fetchone()
    #     if result:
    #         so = result[0]
    #         if so:
    #             domain = [('id', '=', so)]
    #             sale_order_line = self.env['sale.order.line'].search(domain)
    #             warehouse = sale_order_line.order_id.warehouse_id.id
    #     if not self.product_id:
    #         return self.price_unit
    #     original_line = self.move_id.reversed_entry_id.line_ids.filtered(
    #         lambda l: l.display_type == 'cogs' and l.product_id == self.product_id and
    #                   l.product_uom_id == self.product_uom_id and l.price_unit >= 0)
    #     original_line = original_line and original_line[0]
    #     return original_line.price_unit if original_line \
    #         else self.product_id.with_company(self.company_id)._stock_account_get_anglo_saxon_price_unit(
    #         uom=self.product_uom_id, warehouse=warehouse)
    
    def _stock_account_get_anglo_saxon_price_unit(self):
        # * Softhealer code Start *

        #  Passed the warehouse id in _stock_account_get_anglo_saxon_price_unit

        # * Softhealer code end *
        self.ensure_one()
        avg_price=0
        if self.sale_line_ids:
            total_quantity=0
            total_amount=0
            for soline in self.sale_line_ids:
                if soline.move_ids:
                    for sm in soline.move_ids:
                        if sm.stock_valuation_layer_ids:
                            for vl in sm.stock_valuation_layer_ids:
                                if vl.quantity<0:
                                    total_quantity+=vl.quantity
                                    total_amount+=vl.value
            if total_quantity!=0:
                avg_price= total_amount/total_quantity
        else:
             avg_price= self.product_id.with_company(self.company_id)._stock_account_get_anglo_saxon_price_unit(uom=self.product_uom_id)
        
        
        
        original_line = self.move_id.reversed_entry_id.line_ids.filtered(
            lambda l: l.display_type == 'cogs' and l.product_id == self.product_id and
                      l.product_uom_id == self.product_uom_id and l.price_unit >= 0)
        original_line = original_line and original_line[0]
        return original_line.price_unit if original_line \
            else avg_price
        # warehouse = False
        # query = """SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id = %s"""
        # so_query = self._cr.execute(query, [self.id])
        # result = self._cr.fetchone()
        # if result:
        #     so = result[0]
        #     if so:
        #         domain = [('id', '=', so)]
        #         sale_order_line = self.env['sale.order.line'].search(domain)
        #         x
        # if not self.product_id:
        #     return self.price_unit
        # original_line = self.move_id.reversed_entry_id.line_ids.filtered(
        #     lambda l: l.display_type == 'cogs' and l.product_id == self.product_id and
        #               l.product_uom_id == self.product_uom_id and l.price_unit >= 0)
        # original_line = original_line and original_line[0]
        # return original_line.price_unit if original_line \
        #     else self.product_id.with_company(self.company_id)._stock_account_get_anglo_saxon_price_unit(
        #     uom=self.product_uom_id, warehouse=warehouse)


    # Softhealer code
    # def _stock_account_get_anglo_saxon_price_unit(self):
    #     # * Softhealer code Start *
    #
    #     #  Passed the warehouse id in _stock_account_get_anglo_saxon_price_unit
    #
    #     # * Softhealer code end *
    #     self.ensure_one()
    #     warehouse = False
    #     if self.move_id.invoice_origin:
    #         domain = [('name', '=', self.move_id.invoice_origin)]
    #         sale_order = self.env['sale.order'].search(domain)
    #         if sale_order:
    #             warehouse = sale_order.warehouse_id.id
    #     if not self.product_id:
    #         return self.price_unit
    #     original_line = self.move_id.reversed_entry_id.line_ids.filtered(
    #         lambda l: l.display_type == 'cogs' and l.product_id == self.product_id and
    #         l.product_uom_id == self.product_uom_id and l.price_unit >= 0)
    #     original_line = original_line and original_line[0]
    #     return original_line.price_unit if original_line \
    #         else self.product_id.with_company(self.company_id)._stock_account_get_anglo_saxon_price_unit(uom=self.product_uom_id,warehouse=warehouse)