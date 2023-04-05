# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError, Warning


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
    is_truck_invoice_created = fields.Boolean('Truck Invoice Created')

    def action_create_truck_invoice(self):
        invoice_line_ids = []
        product_id = self.env.ref('oe_kemoxon_delivery_custom.product_product_freight_charges')
        move = self.move_ids_without_package[0]
        transport_tolerance = self.transport_tolerance / 100
        sale_price = move.sale_line_id.price_unit

        if not self.transporter:
            raise UserError(_('Please Add Transporter!!'))
        for truck_line in self.truck_transport_details_ids:
            self.is_truck_invoice_created= True
            actual_loss = truck_line.loaded - truck_line.offloaded
            tolerable_loss = transport_tolerance * truck_line.loaded
            loss_in_quantity = tolerable_loss - actual_loss
            loss_in_amount = sale_price * loss_in_quantity

            invoice_line_ids.append((0, 0, {
                'product_id': product_id.id,
                'quantity': truck_line.loaded,
                'price_unit': self.rate,
                'deduction': loss_in_amount
            }))
        self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'date': self.scheduled_date,
                'invoice_date': self.scheduled_date,
                'partner_id': self.transporter.id,
                'invoice_line_ids': invoice_line_ids,
            }
        )

    @api.onchange('consignee')
    def _domain_change(self):
        domain = []
        if self.partner_id:
            if self.partner_id.child_ids:
                domain = self.partner_id.child_ids.ids
                domain.append(self.partner_id.id)
            else:
                domain.append(self.partner_id.id)
        print(domain, 'domaindomain')
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
        for rec in self:
            if rec.quantity_done:
                if rec.sale_line_id:
                    product_uom_qty = rec.sale_line_id.product_uom_qty
                    if rec.sale_line_id.tolerance_type:
                        tolerance_quantity = (product_uom_qty * rec.sale_line_id.tolerance_percentage) / 100
                        if rec.sale_line_id.tolerance_type == 'min_max':
                            if product_uom_qty + tolerance_quantity < rec.quantity_done or product_uom_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.sale_line_id.tolerance_type == 'max':
                            if product_uom_qty + tolerance_quantity < rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.sale_line_id.tolerance_type == 'min':
                            if product_uom_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                elif rec.purchase_line_id:
                    product_qty = rec.purchase_line_id.product_qty
                    if rec.purchase_line_id.tolerance_type:
                        tolerance_quantity = (product_qty * rec.purchase_line_id.tolerance_percentage) / 100
                        if rec.purchase_line_id.tolerance_type == 'min_max':
                            if product_qty + tolerance_quantity < rec.quantity_done or product_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.purchase_line_id.tolerance_type == 'max':
                            if product_qty + tolerance_quantity < rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.purchase_line_id.tolerance_type == 'min':
                            if product_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.constrains('qty_done')
    @api.onchange('qty_done')
    def _check_qty_done(self):
        for rec in self:
            if rec.qty_done:
                if rec.move_id.sale_line_id:
                    product_uom_qty = rec.move_id.sale_line_id.product_uom_qty
                    if rec.move_id.sale_line_id.tolerance_type:
                        tolerance_quantity = (product_uom_qty * rec.move_id.sale_line_id.tolerance_percentage) / 100
                        if rec.move_id.sale_line_id.tolerance_type == 'min_max':
                            if product_uom_qty + tolerance_quantity < rec.qty_done or product_uom_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.sale_line_id.tolerance_type == 'max':
                            if product_uom_qty + tolerance_quantity < rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.sale_line_id.tolerance_type == 'min':
                            if product_uom_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                elif rec.move_id.purchase_line_id:
                    product_qty = rec.move_id.purchase_line_id.product_qty
                    if rec.move_id.purchase_line_id.tolerance_type:
                        tolerance_quantity = (product_qty * rec.move_id.purchase_line_id.tolerance_percentage) / 100
                        if rec.move_id.purchase_line_id.tolerance_type == 'min_max':
                            if product_qty + tolerance_quantity < rec.qty_done or product_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.purchase_line_id.tolerance_type == 'max':
                            if product_qty + tolerance_quantity < rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.purchase_line_id.tolerance_type == 'min':
                            if product_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _(
                                        'Please note that the quantity is not within the tolerance limit of the order.')
                                }}
