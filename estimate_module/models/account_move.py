# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    estimate_id = fields.Many2one('estimate.module', string='Estimate ID', store=True)
    estimate_purchase_line_id = fields.Many2one('estimate.purchase.line', string='Purchase Line ID', store=True)
    estimate_sale_line_id = fields.Many2one('estimate.sale.line', string='Sale Line ID', store=True)
    estimate_cost_line_id = fields.Many2one('estimate.cost.line', string='Cost Line ID', store=True)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        total_qty = 0
        total_costs = 0
        if self.move_type == 'in_invoice':
            for lines in self.invoice_line_ids:
                total_qty += lines.quantity
                total_costs += lines.price_subtotal
            if self.estimate_purchase_line_id and self.estimate_id:
                if self.estimate_id.total_purchase_realized_qty > 0:
                    self.estimate_id.total_purchase_realized_qty += total_qty
                else:
                    self.estimate_id.total_purchase_realized_qty = total_qty
                if self.estimate_id.total_realized_purchases > 0:
                    self.estimate_id.total_realized_purchases += total_costs
                else:
                    self.estimate_id.total_realized_purchases = total_costs

            if self.estimate_cost_line_id and self.estimate_id:
                if self.estimate_id.total_confirmed_costs > 0:
                    self.estimate_id.total_confirmed_costs += total_costs
                else:
                    self.estimate_id.total_confirmed_costs = total_costs
                if self.estimate_id.total_realized_costs > 0:
                    self.estimate_id.total_realized_costs += total_costs
                else:
                    self.estimate_id.total_realized_costs = total_costs
        elif self.move_type == 'out_invoice':
            for lines in self.invoice_line_ids:
                total_qty += lines.quantity
                total_costs += lines.price_subtotal
            if self.estimate_sale_line_id and self.estimate_id:
                if self.estimate_id.total_sale_realized_qty > 0:
                    self.estimate_id.total_sale_realized_qty += total_qty
                else:
                    self.estimate_id.total_sale_realized_qty = total_qty
                if self.estimate_id.total_realized_sales > 0:
                    self.estimate_id.total_realized_sales += total_costs
                else:
                    self.estimate_id.total_realized_sales = total_costs
        elif self.move_type == 'entry':
            for lines in self.invoice_line_ids[0]:
                total_costs += lines.debit
            if self.estimate_cost_line_id and self.estimate_id:
                # if self.estimate_id.total_confirmed_costs > 0:
                #     self.estimate_id.total_confirmed_costs += total_costs
                # else:
                #     self.estimate_id.total_confirmed_costs = total_costs
                if self.estimate_id.total_realized_costs > 0:
                    self.estimate_id.total_realized_costs += total_costs
                else:
                    self.estimate_id.total_realized_costs = total_costs
        return res
