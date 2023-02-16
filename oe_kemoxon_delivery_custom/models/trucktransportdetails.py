from odoo import models, fields, _, api

from odoo.exceptions import UserError


class Truck_Transport_Details(models.Model):
    _name = "truck.transport.details"
    _description = "Truck Transport Details model"
    truck = fields.Char("Truck", required=True)
    trailer = fields.Char()
    driver = fields.Char()
    passport = fields.Char()
    nominated = fields.Float(digits=(3, 3))
    loaded = fields.Float(digits=(3, 3))
    offloaded = fields.Float(digits=(3, 3))
    is_updated = fields.Boolean('Updated', copy=False)
    status = fields.Selection(
        [("Nominated", "Nominated"), ("Waiting to load", "Waiting to load"), ("In transit", "In transit"),
         ("Waiting to offload", "Waiting to offload"), ("Completed", "Completed")])
    statusdate = fields.Date()
    picking_id = fields.Many2one('stock.picking', 'Delivery')
    stock_pick_ids = fields.Many2one("stock.picking", string="Truck Details", required=True)
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    seq = fields.Char("Sequence")
    _sql_constraints = [
        ('checkPrices', 'CHECK(nominated >= 0 AND loaded >=0 AND offloaded>=0 )', 'Quantities cannot be less than 0')
    ]

    def action_print_report(self):
        seq = 0
        for line in self.env['truck.transport.details'].search([('stock_pick_ids', '=', self.env.context.get('p_id'))]):
            seq += 1
            line.seq = "0" + str(seq) if seq < 10 else str(seq)
        return self.env.ref('oe_kemoxon_delivery_custom.action_report_delivery_sale_invoice').report_action(self)

    @api.onchange('offloaded')
    def _get_update_value(self):
        move = self.env['stock.move'].search([('picking_id', '=', self.stock_pick_ids._origin.id)], limit=1)
        if self.offloaded:
            if move and not self.is_updated:
                quantity_done = move.quantity_done
                product_uom_qty = move.product_uom_qty
                if product_uom_qty < self.offloaded + quantity_done:
                    raise UserError(_("You Can't Add Morethan Demand QTy."))
                move.write({
                    'quantity_done': self.offloaded + quantity_done
                })
                self.is_updated = True

    def get_warehouse(self, picking_id=None):
        if picking_id:
            warehouse_obj = self.env['stock.warehouse']
            warehouse_id = warehouse_obj.search([('lot_stock_id', '=', picking_id.location_id.id)])
            result = [warehouse_id.name, warehouse_id.lot_stock_id.display_name]
            return result

    def get_total(self, total=None):
        number = "{:.2f}".format(total)
        return "{:,.2f}".format(float(number))
