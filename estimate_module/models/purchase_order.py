# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    estimate_id = fields.Many2one('estimate.module', string='Estimate ID', store=True)
    estimate_purchase_line_id = fields.Many2one('estimate.purchase.line', string='Purchase Line ID', store=True)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        total_qty = 0
        total_price = 0
        for lines in self.order_line:
            total_qty += lines.product_qty
            total_price += lines.price_subtotal
        if self.estimate_purchase_line_id and self.estimate_id:
            if self.estimate_id.total_purchase_confirmed_qty > 0:
                self.estimate_id.total_purchase_confirmed_qty += total_qty
            else:
                self.estimate_id.total_purchase_confirmed_qty = total_qty
            if self.estimate_id.total_confirmed_purchases > 0:
                self.estimate_id.total_confirmed_purchases += total_price
            else:
                self.estimate_id.total_confirmed_purchases = total_price
        for po_pick in self.picking_ids:
            po_pick.write({'vessel_name': self.estimate_purchase_line_id.vessel_id.vessel_id.vessel_name,
                           'bill_date': self.estimate_purchase_line_id.vessel_id.bl_date,
                           'imo_number': self.estimate_purchase_line_id.vessel_id.vessel_id.imo})
        return res

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        if self.estimate_id and self.estimate_purchase_line_id:
            if self.invoice_ids:
                self.invoice_ids.write({
                    'estimate_id': self.estimate_id.id,
                    'estimate_purchase_line_id': self.estimate_purchase_line_id.id
                })
    #     total_qty = 0
    #     total_price = 0
    #     if res:
    #         for lines in self.order_line:
    #             total_qty += lines.product_qty
    #             total_price += lines.price_subtotal
    #     if self.estimate_purchase_line_id and self.estimate_id:
    #         if self.estimate_id.total_purchase_realized_qty > 0:
    #             self.estimate_id.total_purchase_realized_qty += total_qty
    #         else:
    #             self.estimate_id.total_purchase_realized_qty = total_qty
    #         if self.estimate_id.total_realized_purchases > 0:
    #             self.estimate_id.total_realized_purchases += total_price
    #         else:
    #             self.estimate_id.total_realized_purchases = total_price
        return res
