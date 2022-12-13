# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    bill_date = fields.Date("B/L Date")
    vessel_name = fields.Char("Vessel Name")
    delivery_location = fields.Many2one('delivery.location', "Delivery Location")
    imo_number = fields.Char("IMO Number")
    delivery_from = fields.Date("Delivery From")
    delivery_to = fields.Date('Delivry To')
    truck_transport_details_ids = fields.One2many('truck.transport.details', 'picking_id', "Truck Details")
