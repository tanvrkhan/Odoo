# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError, Warning
import datetime

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
    is_truck_invoice_created = fields.Boolean('Truck Invoice Created', compute='_compute_transport_invoice_count')
    transport_invoice_count = fields.Integer('Truck Invoice Count', compute='_compute_transport_invoice_count')
    allow_validation = fields.Boolean("Allow Validate")
    tt_date = fields.Date('Title Transfer Date')
    incoterm_location_custom = fields.Many2one('incoterm.location', string='Incoterm Location',
                                               related='sale_id.incoterm_location_custom')
    trader = fields.Many2one('hr.employee', string='Trader', related='sale_id.trader')
    en_plus = fields.Boolean('EN Plus')
    custom_delivery_date=fields.Date(string="Delivery Date")
    updatestatus=fields.Char()
    valuation_price = fields.Float(string="Valuation Price")
    def fix_unmatching_lots(self):
        for rec in self:
            for mv in rec.move_ids:
                mv.date = rec.scheduled_date
            if rec.move_ids and rec.env.context.get('check_condition'):
                if self.check_is_return():
                    return super().button_validate()
                else:

                    return rec.check_tolerance_condition()

            else:
                return super().button_validate()
    
    def update_purchase_date_from_corresponding_Lot(self):
        for rec in self:
            if rec.move_ids.quantity_done>0:
                if rec.move_ids.move_line_ids.lot_id:
                    earliest_sale = self.env['stock.move.line'].search([('lot_id','=',rec.move_ids.move_line_ids.lot_id),('quantity_done','<',0)], order = "date asc",limit=1)
                    earliest_date=earliest_sale.date
                    if rec.custom_delivery_date:
                        a=1
                    else:
                        rec.custom_delivery_date = earliest_date + datetime.timedelta(Hours=-1)
            else:
                if rec.move_ids.quantity_done < 0:
                    if rec.move_ids.move_line_ids.lot_id:
                        earliest_sale = self.env['stock.move.line'].search(
                            [('lot_id', '=', rec.move_ids.move_line_ids.lot_id), ('quantity_done', '>', 0)],
                            order="date asc", limit=1)
                        earliest_date = earliest_sale.date
                        if rec.custom_delivery_date:
                            a = 1
                        else:
                            rec.custom_delivery_date = earliest_date + datetime.timedelta(Hours=1)
    def set_delivery_date(self):
        for rec in self:
            if rec.scheduled_date and rec.date_deadline:
                if rec.scheduled_date<rec.date_deadline:
                    rec.custom_delivery_date = rec.scheduled_date
                elif rec.date_deadline< rec.scheduled_date:
                    rec.scheduled_date = rec.date_deadline
                    rec.custom_delivery_date = rec.date_deadline
                
    def button_validate(self):
        for rec in self:
            if rec.move_ids.move_line_ids.lot_id:
                r= super(StockPicking,rec)._action_done()
            else:
                lot_name='NA'
                found_lot = self.env['stock.lot'].search([('name','=','NA'),('product_id','=',rec.product_id.id)])
                if found_lot:
                    rec.move_ids.move_line_ids.lot_id =found_lot
                else:
                    new_lot = self.env['stock.lot'].create(
                        {
                            'product_id': rec.product_id.id,
                            'name': 'NA'
                        })
                    rec.move_ids.move_line_ids.lot_id = new_lot
                r = super(StockPicking, rec)._action_done()
    def button_confirm(self):
        for rec in self:
            return super().action_confirm()
        
    def button_cancel(self):
        for rec in self:
            return super().action_cancel()

    def check_is_return(self):
        for rec in self:
            if rec.move_ids:
                if rec.picking_type_code == 'incoming' or 'outgoing' and rec.move_ids[0].state == 'done' \
                        and rec.move_ids[0].scrapped:
                    return True
                else:
                    return False
            else:
                return False

    def check_tolerance_condition(self):
        for rec in self:
            move = rec.move_ids[0]
            with_tol_allwd_qty, tol_type, is_tol = rec.get_tolerance_val(move)
            if not is_tol:
                with_tol_allwd_qty = move.product_uom_qty
            all_done_qty = sum(
                move.picking_id.move_line_ids_without_package.mapped('qty_done'))

            if tol_type == 'min' and all_done_qty < with_tol_allwd_qty:
                name = 'Warning'
                message = _(
                    'Please note that the quantity is not within the tolerance limit of the order. \n'
                    f'allowed quantity {with_tol_allwd_qty} remaining quantity {with_tol_allwd_qty - all_done_qty}')
                return self.env['wk.wizard.message'].genrated_message(message, name)

            elif tol_type == 'max' and all_done_qty > with_tol_allwd_qty:
                name = 'Warning'
                message = _(
                    'Please note that the quantity is not within the tolerance limit of the order.\n'
                    f'allowed quantity {with_tol_allwd_qty}'
                )
                return self.env['wk.wizard.message'].genrated_message(message, name)

            elif tol_type == 'both' and (all_done_qty > with_tol_allwd_qty.get(
                    'max') or all_done_qty < with_tol_allwd_qty.get('min')):
                message = _(
                    'Please note that the quantity is not within the tolerance limit of the order.\n'
                    f'Max quantity: {with_tol_allwd_qty.get("max")}\n'
                    f'Min Quantity {with_tol_allwd_qty.get("min")}\n'
                    f'Max Remaining {with_tol_allwd_qty.get("max") - all_done_qty}'
                )
                name = 'Warning'
                return self.env['wk.wizard.message'].genrated_message(message, name)

            elif not tol_type and (all_done_qty > with_tol_allwd_qty or all_done_qty < with_tol_allwd_qty):
                name = "Warning"
                message = f"Please note that the quantity is not within the tolerance limit of the order ," \
                          f" max allowed {with_tol_allwd_qty} min allowed {with_tol_allwd_qty}"
                return self.env['wk.wizard.message'].genrated_message(message, name)

            else:
                return self.with_context(check_condition=0).button_validate()

    @staticmethod
    def get_tolerance_val(move=None):
        for rec in move:
            if rec.sale_line_id or rec.purchase_line_id:
                product_uom_qty = rec.sale_line_id.product_uom_qty or rec.purchase_line_id.product_uom_qty
                if rec.sale_line_id.tolerance_type or rec.purchase_line_id.tolerance_type:
                    tolerance_quantity = (product_uom_qty * rec.sale_line_id.tolerance_percentage) / 100 \
                        if rec.sale_line_id \
                        else (product_uom_qty * rec.purchase_line_id.tolerance_percentage) / 100

                    if rec.sale_line_id.tolerance_type or rec.purchase_line_id.tolerance_type == 'min':
                        return product_uom_qty - tolerance_quantity, 'min', True
                    elif rec.sale_line_id.tolerance_type or rec.purchase_line_id.tolerance_type == 'max':
                        return product_uom_qty + tolerance_quantity, 'max', True
                    else:
                        return {'min': product_uom_qty - tolerance_quantity,
                                'max': product_uom_qty + tolerance_quantity}, 'both', True
                else:
                    return False, False, False
        else:
            return False, False, False

    def _compute_transport_invoice_count(self):
        for rec in self:
            moves = self.env['account.move'].search([('transporter_details_id', '=', self.id)])
            if moves:
                rec.transport_invoice_count = len(moves)
                rec.is_truck_invoice_created = True
            else:
                rec.transport_invoice_count = 0
                rec.is_truck_invoice_created = False

    def action_create_truck_invoice(self):

        product_id = self.env.ref('oe_kemoxon_delivery_custom.product_product_freight_charges')
        move = self.move_ids_without_package[0]
        transport_tolerance = self.transport_tolerance / 100
        sale_price = move.sale_line_id.price_unit

        transporterids = []
        invoice_details_dict = {}
        transporter_invoices = []
        for truck_line in self.truck_transport_details_ids:
            if not truck_line.transporter:
                raise UserError(_('Please Add Transporter!!'))
            if truck_line.transporter.id not in transporterids:
                transporterids.append(truck_line.transporter.id)
                invoice_details_dict[truck_line.transporter.id] = {
                    'lines': [truck_line]
                }
            else:
                invoice_details_dict[truck_line.transporter.id]['lines'].append(truck_line)
        for transporterid in transporterids:
            invoice_line_ids = []
            for line in invoice_details_dict.get(transporterid).get('lines'):
                actual_loss = line.loaded - line.offloaded
                tolerable_loss = transport_tolerance * line.loaded
                loss_in_quantity = tolerable_loss - actual_loss
                loss_in_amount = sale_price * loss_in_quantity
                if line.offloaded > line.loaded:
                    loss_in_amount = 0

                invoice_line_ids.append((0, 0, {
                    'product_id': product_id.id,
                    'name': line.truck,
                    'quantity': line.loaded,
                    'price_unit': self.rate,
                    'deduction': loss_in_amount,
                }))
            account_move = self.env['account.move'].create(
                {
                    'move_type': 'in_invoice',
                    'date': self.scheduled_date,
                    'invoice_date': self.scheduled_date,
                    'partner_id': transporterid,
                    'invoice_line_ids': invoice_line_ids,
                    'transporter_details_id': self.id,
                    'invoice_payment_term_id': self.transporter_payment_terms.id if self.transporter_payment_terms else False

                }
            )

    def set_reserved_zero(self):
        for record in self:
            for move in record.move_ids:
                for line in move.move_line_ids:
                    line.reserved_uom_qty=0

    def action_view_transporter_invoice(self):
        action = {
            'domain': [('transporter_details_id', '=', self.id)],
            'name': 'Transporter Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
        }
        return action

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

    def set_stock_move_to_draft(self):
        for record in self:
            existingstate= record.state
            am = record.move_ids.stock_valuation_layer_ids.account_move_id
            am.line_ids.remove_move_reconcile()
            am.button_draft()
            am.unlink()
            moves = record.move_ids
            # for ae in record.move_ids.stock_valuation_layer_ids.account_move_id.line_ids:
            #     ae.remove_move_reconcile()
            # record.move_ids.stock_valuation_layer_ids.account_move_id.line_ids.unlink()
            # record.move_ids.stock_valuation_layer_ids.account_move_id.unlink()
            moves.stock_valuation_layer_ids.unlink()
            record.state = 'draft'
            moves.move_line_ids.state = 'draft'
            moves.state = 'draft'
            moves.state = 'draft'
            
            for line in record.move_ids.move_line_ids:
                if line.lot_id:
                    previous_lot = line.lot_id
                    lotNumbers = self.env['stock.lot'].search(
                        [('product_id', '=', line.product_id.id), ('name', '=', line.lot_id.name)])
                    if lotNumbers:
                        line.lot_id = lotNumbers[0]
                    else:
                        new_lot= self.env['stock.lot'].create({
                            'product_id': line.product_id.id,
                            'name': previous_lot.name,
                            'company_id': line.company_id.id
                        })
                        line.lot_id=new_lot
                        record.move_ids.move_line_ids.product_id = record.move_ids.product_id
            
            for line in record.move_ids.move_line_ids:
                if line.qty_done != 0 and existingstate == 'done':
                    location_quant = record.env['stock.quant'].search(['&', ('product_id', '=', record.product_id.id)
                                                                        , ('lot_id', '=', line.lot_id.id)
                                                                        , ('location_id', '=', line.location_id.id)

                                                                          # , ('company_id', '=', line.company_id.id)
                                                                     ])
                    location_dest_quant = record.env['stock.quant'].search(['&', ('product_id', '=', record.product_id.id)
                                                                             , ('lot_id', '=', line.lot_id.id)
                                                                             ,
                                                                          ('location_id', '=', line.location_dest_id.id)
                                                                          # , ('company_id', '=', line.company_id.id)
                                                                          ])

                    if len(location_quant) == 1:
                        if (location_quant.location_id.usage == 'internal'):
                            if (existingstate == 'done'):
                            # SALES REVERSAL
                                record.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                                   package_id=None, owner_id=None,
                                                                                   location_id=line.location_id,
                                                                                   quantity=line.qty_done,
                                                                                   lot_id=line.lot_id, in_date=None)
                        # location_quant.quantity=location_quant.quantity-line.qty_done
                        else:
                            # PURCHASE REVERSAL
                            if (existingstate == 'done'):
                                record.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                               package_id=None, owner_id=None,
                                                                               location_id=line.location_id,
                                                                               quantity=line.qty_done,
                                                                               lot_id=line.lot_id, in_date=None)

                    if len(location_dest_quant) == 1:
                        if (location_quant.location_id.usage == 'internal'):
                            # PURCHASE REVERSAL
                            if (existingstate == 'done'):
                                record.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                               package_id=None, owner_id=None,
                                                                               location_id=line.location_dest_id,
                                                                               quantity=-1 * line.qty_done,
                                                                               lot_id=line.lot_id, in_date=None)
                        # location_dest_quant.quantity=location_dest_quant.quantity-line.qty_done
                        else:
                            # PURCHASE REVERSAL
                            if (existingstate == 'done'):
                                record.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                               package_id=None, owner_id=None,
                                                                               location_id=line.location_dest_id,
                                                                               quantity=-1 * line.qty_done,
                                                                               lot_id=line.lot_id, in_date=None)
            record.updatestatus="waspostedbefore"

    def sync_stock_quant(self):
        company = self.env.company.id
        quants=self.env['stock.quant'].search([('product_id','=',self.product_id.id)]).unlink()
        # if quants:
        #     for quant in quants:
        #         quant.unlink()
        
        pickings = self.env['stock.picking'].search([('product_id','=',self.product_id.id)])
        for record in pickings:
            for line in record.move_ids.move_line_ids:
                # check if move is in state done and quantity is not 0.
                if line.qty_done != 0 and line.state == 'done' and line.product_id.type=='product':
                    location_quant = self.env['stock.quant'].search(['&', ('product_id', '=', line.product_id.id)
                                                                        , ('lot_id', '=', line.lot_id.id)
                                                                        , ('location_id', '=', line.location_id.id)
                                                                     # ,('company_id','=',line.company_id.id)
                                                                     ])
                    # if entry already exists, update it.
                    if location_quant:
                        self.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                           package_id=None, owner_id=None,
                                                                           location_id=line.location_id,
                                                                           quantity=-1 * line.qty_done,
                                                                           lot_id=line.lot_id, in_date=None)
                    # otherwise create it.
                    else:
                        self.env['stock.quant'].create({
                            'product_id': line.product_id.id,
                            'location_id': line.location_id.id,
                            'lot_id': line.lot_id.id,
                            'quantity': -1 * line.qty_done,
                            # 'company_id':line.company_id.id
                        })
                    location_dest_quant = self.env['stock.quant'].search(['&','&', ('product_id', '=', line.product_id.id)
                                                                             , ('lot_id', '=', line.lot_id.id)
                                                                             # ,('company_id','=',line.company_id.id)
                                                                          ,('location_id', '=', line.location_dest_id.id)
                                                                          ])
                    if location_dest_quant:
                        self.env['stock.quant']._update_available_quantity(product_id=line.product_id,
                                                                           package_id=None, owner_id=None,
                                                                           location_id=line.location_dest_id,
                                                                           quantity=1 * line.qty_done,
                                                                           lot_id=line.lot_id, in_date=None)
                    # otherwise create it.
                    else:
                        self.env['stock.quant'].create({
                            'product_id': line.product_id.id,
                            'location_id': line.location_dest_id.id,
                            'lot_id': line.lot_id.id,
                            'quantity': line.qty_done,
                            # 'company_id':line.company_id.id
                        })

    def stock_quant_zero(self):
        all_quant = self.env['stock.quant'].search([])
        for quant in all_quant:
            quant.quantity = 0

    def delete_all_inventory_adjustments(self):
        all_moves = self.env['stock.move'].search([])
        for move in all_moves:
            if move.picking_id:
                pass
            else:
                move.stock_valuation_layer_ids.account_move_id.state = 'draft'
                move.stock_valuation_layer_ids.account_move_id.line_ids.unlink()
                move.stock_valuation_layer_ids.account_move_id.unlink()
                move.stock_valuation_layer_ids.unlink()
                move.state = 'draft'
                move.move_line_ids.state = 'draft'
                move.move_line_ids.unlink()
                move.unlink()

    def delete_all_internal_transfers(self):
        all_pickings = self.env['stock.picking'].search([('picking_type_id.code', '=', 'internal')])
        for picking in all_pickings:
            picking.move_ids.stock_valuation_layer_ids.account_move_id.state = 'draft'
            picking.move_ids.stock_valuation_layer_ids.account_move_id.line_ids.unlink()
            picking.move_ids.stock_valuation_layer_ids.account_move_id.unlink()
            picking.move_ids.stock_valuation_layer_ids.unlink()
            picking.move_ids.state = 'draft'
            picking.move_ids.move_line_ids.state = 'draft'
            picking.move_ids.move_line_ids.unlink()
            picking.move_ids.unlink()

    def fix_valuation_warehouse(self):
        for rec in self:
            if rec.location_id.usage=='internal':
                rec.move_ids.stock_valuation_layer_ids.warehouse_id = rec.location_id.warehouse_id.id
            elif rec.location_dest_id.usage=='internal':
                rec.move_ids.stock_valuation_layer_ids.warehouse_id = rec.location_dest_id.warehouse_id.id
    def update_valuation(self):
        self.move_ids.stock_valuation_layer_ids.unit_cost = self.valuation_price
        self.move_ids.stock_valuation_layer_ids.value = self.valuation_price * self.move_ids.stock_valuation_layer_ids.quantity
        
    
# search where location id is 8 and add it to a collection
# search where location id is not 8 and is internal location
# updates the ones with 8

# or (lot.delivery_ids.location_id!=8 and lot.delivery_ids.location_dest_id==8):


class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    truck_detail_ref = fields.Integer("Truck Detail Id")
    delete_option = fields.Boolean("Delete Option", default=True)

    @api.onchange('qty_done')
    def _oe_onchange_qty_done(self):
        for rec in self:
            related_truck_details = self.env['truck.transport.details'].search([
                ('stock_pick_ids', '=', rec.picking_id._origin.id), ('truck_detail_ref', '=', rec.truck_detail_ref)])
            if not related_truck_details:
                related_truck_details = self.env['truck.transport.details'].search([
                    ('truck_detail_ref', '=', rec.truck_detail_ref)])
            if related_truck_details:
                related_truck_details.offloaded = rec.qty_done

    def unlink(self):
        for rec in self:
            rec.delete_option = False
            related_truck_details = self.env['truck.transport.details'].search([
                ('stock_pick_ids', '=', rec.picking_id.id), ('truck_detail_ref', '=', rec.truck_detail_ref)])
            if related_truck_details and related_truck_details.delete_option:
                related_truck_details.unlink()
        return super(StockMoveLine, self).unlink()
    
