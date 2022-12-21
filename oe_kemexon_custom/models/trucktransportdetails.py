from odoo import models, fields, _
from odoo.exceptions import UserError


class Truck_Transport_Details(models.Model):
    _name = "truck.transport.details"
    _description = "Truck Transport Details model"
    truck = fields.Char("Truck", required=True)
    trailer = fields.Char()
    driver = fields.Char()
    passport = fields.Char()
    nominated = fields.Float()
    loaded = fields.Float()
    offloaded = fields.Float()
    is_updated = fields.Boolean('Updated')
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

    def action_update_qty(self):
        move = self.env['stock.move'].search([('picking_id', '=', self.stock_pick_ids.id)], limit=1)
        if move and not self.is_updated:
            quantity_done = move.quantity_done
            product_uom_qty = move.product_uom_qty
            if product_uom_qty < self.offloaded + quantity_done:
                raise UserError(_("You Can't Add Morethan Demand QTy."))
            move.write({
                'quantity_done': self.offloaded + quantity_done
            })
            self.is_updated = True
