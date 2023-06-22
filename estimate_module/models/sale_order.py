# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    estimate_id = fields.Many2one('estimate.module', string='Estimate ID', store=True)
    estimate_sale_line_id = fields.Many2one('estimate.sale.line', string='Sale Line ID', store=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        total_qty = 0
        total_price = 0
        for lines in self.order_line:
            total_qty += lines.product_uom_qty
            total_price += lines.price_subtotal
        if self.estimate_sale_line_id and self.estimate_id:
            if self.estimate_id.total_sale_confirmed_qty > 0:
                self.estimate_id.total_sale_confirmed_qty += total_qty
            else:
                self.estimate_id.total_sale_confirmed_qty = total_qty
            if self.estimate_id.total_confirmed_sales > 0:
                self.estimate_id.total_confirmed_sales += total_price
            else:
                self.estimate_id.total_confirmed_sales = total_price
        for so_pick in self.picking_ids:
            so_pick.write({'vessel_name': self.estimate_sale_line_id.vessel_id.vessel_id.vessel_name,
                           'bill_date': self.estimate_sale_line_id.vessel_id.bl_date,
                           'imo_number': self.estimate_sale_line_id.vessel_id.vessel_id.imo})
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        res = super(SaleOrder, self)._create_invoices()
        if self.estimate_id and self.estimate_sale_line_id:
            if res:
                res.write({
                    'estimate_id': self.estimate_id.id,
                    'estimate_sale_line_id': self.estimate_sale_line_id.id
                })
        # total_qty = 0
        # total_price = 0
        # if res:
        #     for lines in self.order_line:
        #         total_qty += lines.product_uom_qty
        #         total_price += lines.price_subtotal
        # if self.estimate_sale_line_id and self.estimate_id:
        #     if self.estimate_id.total_sale_realized_qty > 0:
        #         self.estimate_id.total_sale_realized_qty += total_qty
        #     else:
        #         self.estimate_id.total_sale_realized_qty = total_qty
        #     if self.estimate_id.total_realized_sales > 0:
        #         self.estimate_id.total_realized_sales += total_price
        #     else:
        #         self.estimate_id.total_realized_sales = total_price
        return res

