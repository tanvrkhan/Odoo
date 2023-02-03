# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    bill_date = fields.Date("B/L Date")
    vessel_name = fields.Char("Vessel Name")
    delivery_location = fields.Many2one('delivery.location', "Delivery Location")
    imo_number = fields.Char("IMO Number")
    delivery_from = fields.Date("Delivery From")
    delivery_to = fields.Date('Delivry To')
    truck_transport_details_ids = fields.One2many('truck.transport.details', 'stock_pick_ids', "Truck Details")
    transporter = fields.Many2one('res.partner', 'Transporter')
    consignee = fields.Many2one('res.partner', 'Consignee')
    transporter_payment_terms = fields.Many2one('account.payment.term', 'Transporter Payment Terms')
    rate = fields.Float('Rate')
    transport_tolerance = fields.Float('Transport Tolerance')

    @api.onchange('consignee')
    def _domain_change(self):
        domain = []
        if self.partner_id:
            if self.partner_id.child_ids:
                domain = self.partner_id.child_ids.ids
                domain.append(self.partner_id.id)
            else:
                domain.append(self.partner_id.id)
        return {
            'domain': {
                'consignee': [('id', 'in', domain)]}
        }


class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.constrains('quantity_done')
    @api.onchange('quantity_done')
    def _check_quantity_done(self):
        if self.quantity_done:
            if self.sale_line_id:
                product_uom_qty = self.sale_line_id.product_uom_qty
                if self.sale_line_id.tolerance_type:
                    if self.sale_line_id.tolerance_type == 'min_max':
                        if product_uom_qty + self.sale_line_id.tolerance_percentage < self.quantity_done or product_uom_qty - self.sale_line_id.tolerance_percentage > self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
                    elif self.sale_line_id.tolerance_type == 'max':
                        if product_uom_qty + self.sale_line_id.tolerance_percentage < self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
                    elif self.sale_line_id.tolerance_type == 'min':
                        if product_uom_qty - self.sale_line_id.tolerance_percentage > self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
            elif self.purchase_line_id:
                product_qty = self.purchase_line_id.product_qty
                if self.purchase_line_id.tolerance_type:
                    if self.purchase_line_id.tolerance_type == 'min_max':
                        if product_qty + self.purchase_line_id.tolerance_percentage < self.quantity_done or product_qty - self.sale_line_id.tolerance_percentage > self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
                    elif self.purchase_line_id.tolerance_type == 'max':
                        if product_qty + self.purchase_line_id.tolerance_percentage < self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
                    elif self.purchase_line_id.tolerance_type == 'min':
                        if product_qty - self.purchase_line_id.tolerance_percentage > self.quantity_done:
                            raise UserError(_("You cannot Allow This Quantity."))
