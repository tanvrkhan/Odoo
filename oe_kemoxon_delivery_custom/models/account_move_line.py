# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models


class UpdateInvoiceCosting(models.Model):
    _inherit = 'account.move.line'

    
        
       
    def reset_to_draft(self) :
        for rec in self:
            rec.move_id.button_draft()
            rec.move_id.button_cancel()
    
    def update_accounts_from_product(self):
        for rec in self:
            if rec.product_id.name=="Down payment" and "sale" in rec.account_id.name and rec.display_type=="product":
                if rec.move_id.move_type=="in_invoice" or rec.move_id.move_type=="out_refund":
                    rec.account_id = rec.product_id.property_account_expense_id
                elif rec.move_id.move_type=="out_invoice" or rec.move_id.move_type=="in_refund":
                    rec.account_id = rec.product_id.property_account_income_id
        

        
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