from copy import copy
from email.policy import default
from operator import truediv
from typing_extensions import Required
from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError


class Truck_Transport_Details(models.Model):
    _name = "truck.transport.details"
    _description = "Truck Transport Details model"
    truck = fields.Char("Truck", required=True)
    trailer = fields.Char()
    driver = fields.Char()
    passport = fields.Char()
    nominated = fields.Float()
    loaded = fields.Float()
    is_add_report = fields.Boolean('Add Report')
    offloaded = fields.Float()
    status = fields.Selection(
        [("Nominated", "Nominated"), ("Waiting to load", "Waiting to load"), ("In transit", "In transit"),
         ("Waiting to offload", "Waiting to offload"), ("Completed", "Completed")])
    statusdate = fields.Date()
    picking_id = fields.Many2one('stock.picking', 'Delivery')
    stock_pick_ids = fields.Many2one("stock.picking", string="Truck Details", required=True)
    _sql_constraints = [
        ('checkPrices', 'CHECK(nominated >= 0 AND loaded >=0 AND offloaded>=0 )', 'Quantities cannot be less than 0')
    ]

    def action_print_report(self):
        return self.env.ref('oe_kemexon_custom.action_report_delivery_sale_invoice').report_action(self)
