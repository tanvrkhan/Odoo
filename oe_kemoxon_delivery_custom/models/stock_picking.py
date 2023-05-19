# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError,Warning


class StockPicking(models.Model):
    _inherit = "stock.picking"

    bill_date = fields.Date("B/L Date")
    vessel_name = fields.Char("Vessel Name")
    delivery_location = fields.Many2one(string="Delivery Location", related='sale_id.delivery_location')
    imo_number = fields.Char("IMO Number")
    delivery_from = fields.Date(string="Delivery From", related='sale_id.delivery_from')
    delivery_to = fields.Date(string="To", related='sale_id.delivery_to')
    truck_transport_details_ids = fields.One2many('truck.transport.details', 'stock_pick_ids', "Truck Details")
    transporter = fields.Many2one('res.partner', 'Transporter')
    consignee = fields.Many2one('res.partner', 'Consignee')
    transporter_payment_terms = fields.Many2one('account.payment.term', 'Transporter Payment Terms')
    rate = fields.Float('Rate')
    transport_tolerance = fields.Float('Transport Tolerance')
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    vessel_ids = fields.One2many('vessel.information', 'stock_pick_ids', "Vessel Details")

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
