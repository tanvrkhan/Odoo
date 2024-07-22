# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    incoterm_location2 = fields.Many2one('incoterm.location', string='Incoterm Location')
    incoterm_location_custom = fields.Many2one('incoterm.location', string='Incoterm Location')
    status_custom = fields.Selection([('open', 'Open'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], string='Status')
    trader = fields.Many2one('hr.employee', string='Trader')
    en_plus = fields.Boolean('EN Plus')
class SaleOrder(models.Model):
    _inherit = "sale.order"

    deal_ref = fields.Char("Deal Ref")
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    delivery_from = fields.Date("Delivery From")
    delivery_to = fields.Date('Delivry To')
    delivery_location = fields.Many2one('delivery.location', "Delivery Location")
    incoterm_location2 = fields.Many2one('incoterm.location', string='Incoterm Location')
    incoterm_location_custom = fields.Many2one('incoterm.location', string='Incoterm Location')
    status_custom = fields.Selection([('open', 'Open'), ('closed', 'Closed'), ('pfi', 'PFI'), ('cancelled', 'Cancelled')], string='Status')
    trader = fields.Many2one('hr.employee', string='Trader')
    legal_entity = fields.Many2one('legal.entity', string='Representing Entity')
    show_vat_ids = fields.Boolean('Show VAT ID')
    en_plus = fields.Boolean('EN Plus')
    show_hs_code = fields.Boolean('Show HS Code')
    show_product_origin = fields.Boolean('Show Product Origin')
    company_bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Company Bank Account',
        related='partner_id.company_bank_account_id',
        readonly=True,
    )

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['deal_ref'] = self.deal_ref
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tolerance_type = fields.Selection([('min_max', 'Min/Max'), ('max', 'Max'), ('min', 'Min')],
                                      string='Tolerance Type')
    tolerance_percentage = fields.Float("Tolerance Percentage")
    product_origin = fields.Char("Product Origin")

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        return res

    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        return result




#
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    tolerance_type = fields.Selection([('min_max', 'Min/Max'), ('max', 'Max'), ('min', 'Min')],
                                      string='Tolerance Type')
    tolerance_percentage = fields.Float("Tolerance Percentage")

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
        return res

    def write(self, vals):
        result = super(PurchaseOrderLine, self).write(vals)
        return result


