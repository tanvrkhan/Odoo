from odoo import models, fields, _, api

from odoo.exceptions import UserError


class TruckTransportDetails(models.Model):
    _name = "truck.transport.details"
    _description = "Truck Transport Details model"
    _sql_constraints = [
        ('checkPrices', 'CHECK(nominated >= 0 AND loaded >=0 AND offloaded>=0 )', 'Quantities cannot be less than 0')
    ]

    transporter = fields.Many2one("res.partner", "Transporter")
    truck = fields.Char("Truck", required=True)
    trailer = fields.Char()
    driver = fields.Char()
    passport = fields.Char()
    nominated = fields.Float(digits=(3, 3))
    loaded = fields.Float(digits=(3, 3))
    offloaded = fields.Float(digits=(3, 3))
    is_updated = fields.Boolean('Updated', copy=False)
    date = fields.Date('Date')
    status = fields.Selection(
        [("Nominated", "Nominated"), ("Waiting to load", "Waiting to load"), ("In transit", "In transit"),
         ("Waiting to offload", "Waiting to offload"), ("Completed", "Completed")])
    statusdate = fields.Date()
    picking_id = fields.Many2one('stock.picking', 'Delivery')
    stock_pick_ids = fields.Many2one("stock.picking", string="Truck Details", required=True)
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    seq = fields.Char("Sequence")
    truck_detail_ref = fields.Integer("Move Link Ref")
    delete_option = fields.Boolean("Delete Option", default=True)

    def action_print_report(self):
        seq = 0
        for line in self.env['truck.transport.details'].search([('stock_pick_ids', '=', self.env.context.get('p_id'))]):
            seq += 1
            line.seq = "0" + str(seq) if seq < 10 else str(seq)
        return self.env.ref('oe_kemoxon_delivery_custom.action_report_delivery_sale_invoice').report_action(self)

    @api.onchange("offloaded")
    def _onchange_offload(self):
        for rec in self:
            move = self.env['stock.move'].search([('picking_id', '=', rec.stock_pick_ids._origin.id)], limit=1)
            if move and rec.offloaded > 0:
                with_tol_allwd_qty, tol_type, is_tol = rec.get_tolerance_val(move)
                if not is_tol:
                    with_tol_allwd_qty = move.product_uom_qty
                current_rel_ml_qty = rec.get_current_mv_line(rec, move)
                all_done_qty = sum(
                    move.picking_id.move_line_ids_without_package.mapped('qty_done')) - current_rel_ml_qty
                if tol_type == 'min' and all_done_qty + rec.offloaded < with_tol_allwd_qty:
                    rec.create_mv_line(rec, move)
                    return {'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'Please note that the quantity is not within the tolerance limit of the order. \n'
                            f'allowed quantity {with_tol_allwd_qty} remaining quantity {with_tol_allwd_qty - all_done_qty}'
                        )
                    }}
                elif tol_type == 'max' and all_done_qty + rec.offloaded > with_tol_allwd_qty:
                    rec.create_mv_line(rec, move)
                    return {'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'Please note that the quantity is not within the tolerance limit of the order.\n'
                            f'allowed quantity {with_tol_allwd_qty}')
                    }}

                elif tol_type == 'both' and (all_done_qty + rec.offloaded > with_tol_allwd_qty.get(
                        'max') or all_done_qty + rec.offloaded < with_tol_allwd_qty.get('min')):
                    rec.create_mv_line(rec, move)
                    return {'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'Please note that the quantity is not within the tolerance limit of the order.\n'
                            f'Max quantity: {with_tol_allwd_qty.get("max")}\n'
                            f'Min Quantity {with_tol_allwd_qty.get("min")}\n'
                            f'Max Remaining {with_tol_allwd_qty.get("max") - all_done_qty}'
                        )
                    }}
                else:
                    rec.create_mv_line(rec, move)

    def get_current_mv_line(self, rec=None, move=None):
        move_line = self.env['stock.move.line'].search(
            [('picking_id', '=', move.picking_id.id),
             ('truck_detail_ref', '=', rec.truck_detail_ref)])
        if move_line:
            return move_line.qty_done
        return 0

    def create_mv_line(self, rec=None, move=None):
        if not rec.truck_detail_ref or rec.truck_detail_ref not in move.picking_id.move_line_ids_without_package.mapped(
                'truck_detail_ref') and rec.offloaded > 0:
            all_truck_detail_ref = move.picking_id.move_line_ids_without_package.mapped(
                'truck_detail_ref')
            target_number = 1 if not all_truck_detail_ref else max(all_truck_detail_ref) + 1
            move.picking_id.move_line_ids_without_package = [(0, 0, {
                'company_id': rec.env.company.id,
                'location_id': move.picking_id.location_id.id,
                'location_dest_id': move.picking_id.location_dest_id.id,
                'product_id': move.picking_id.move_ids_without_package[0].product_id.id,
                'product_uom_id': move.picking_id.move_ids_without_package[0].product_uom.id,
                'qty_done': rec.offloaded,
                'truck_detail_ref': target_number
            })]
            rec.truck_detail_ref = target_number
            rec.picking_id = move.picking_id.id

        else:
            move_line = self.env['stock.move.line'].search(
                [('picking_id', '=', move.picking_id.id),
                 ('truck_detail_ref', '=', rec.truck_detail_ref)])
            if move_line:
                move_line.write({
                    'qty_done': rec.offloaded,
                })

    @staticmethod
    def get_tolerance_val(move=None):
        for rec in move:
            if rec.sale_line_id:
                product_uom_qty = rec.sale_line_id.product_uom_qty
                if rec.sale_line_id.tolerance_type:
                    tolerance_quantity = (product_uom_qty * rec.sale_line_id.tolerance_percentage) / 100
                    if rec.sale_line_id.tolerance_type == 'min':
                        return product_uom_qty - tolerance_quantity, 'min', True
                    elif rec.sale_line_id.tolerance_type == 'max':
                        return product_uom_qty + tolerance_quantity, 'max', True
                    else:
                        return {'min': product_uom_qty - tolerance_quantity,
                                'max': product_uom_qty + tolerance_quantity}, 'both', True
                else:
                    return False, False, False

    def unlink(self):
        for rec in self:
            rec.delete_option = False
            move_line = self.env['stock.move.line'].search(
                [('picking_id', '=', rec.stock_pick_ids.id), ('truck_detail_ref', '=', rec.truck_detail_ref)])
            if move_line and move_line.delete_option:
                move_line.unlink()
        return super(TruckTransportDetails, self).unlink()

    def get_warehouse(self, picking_id=None):
        if picking_id:
            warehouse_obj = self.env['stock.warehouse']
            warehouse_id = warehouse_obj.search([('lot_stock_id', '=', picking_id.location_id.id)])
            result = [warehouse_id.name, warehouse_id.lot_stock_id.display_name]
            return result

    def get_total(self, total=None):
        number = "{:.2f}".format(total)
        return "{:,.2f}".format(float(number))
