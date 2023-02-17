# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    deal_ref = fields.Char("Deal Ref")
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    delivery_from = fields.Date("Delivery From")
    delivery_to = fields.Date('Delivry To')
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['deal_ref'] = self.deal_ref
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tolerance_type = fields.Selection([('min_max', 'Min/Max'), ('max', 'Max'), ('min', 'Min')],
                                      string='Tolerance Type')
    tolerance_percentage = fields.Float("Tolerance Percentage")

#
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    tolerance_type = fields.Selection([('min_max', 'Min/Max'), ('max', 'Max'), ('min', 'Min')],
                                      string='Tolerance Type')
    tolerance_percentage = fields.Float("Tolerance Percentage")
