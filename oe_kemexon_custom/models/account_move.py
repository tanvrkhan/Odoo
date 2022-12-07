# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    deal_ref = fields.Char("Deal Ref")
    bill_date = fields.Date("B/L Date", related='picking_id.bill_date')
    vessel_name = fields.Char("Vessel Name", related='picking_id.vessel_name')
    delivery_location = fields.Many2one('delivery.location', "Delivery Location",
                                        related='picking_id.delivery_location')
    picking_id = fields.Many2one('stock.picking', "Delivery Order")

    journal_id = fields.Many2one('account.journal', string='Journal', domain=[], required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True)


class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")
