# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(InheritPurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty,
                                                                             product_uom)
        partner = self.partner_id.x_studio_quick_name
        year = str(self.order_id.date_order.year)[2:]
        month = self.order_id.date_order.month
        if (month < 10):
            month = "0" + str(month)
        else:
            str(month)
        datepart = str(year) + str(month)
        if self.analytic_distribution:
            analytic_account_keys = self.analytic_distribution.keys()
            if analytic_account_keys:
                for key in analytic_account_keys:
                    analytic_account = self.env['account.analytic.account'].search([('id', '=', key), ])
                    analytic_name = analytic_account.name
                    lot_number = partner + "-" + datepart + "-" + analytic_name
                    lot_id = self.env['stock.lot'].create(
                        {'name': lot_number, 'product_id': self.product_id.id, 'company_id': self.company_id.id})
                    lot_to_add = (4, lot_id.id)
                    if ('lot_ids' in res):
                        res['lot_ids'].append(lot_to_add)
                    else:
                        res['lot_ids'] = lot_to_add
                        res['lot_id_custom'] = lot_id.id
                    return res



