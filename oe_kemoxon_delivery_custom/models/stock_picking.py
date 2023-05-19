# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError, Warning


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
                    'deduction': loss_in_amount
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
            # transporter_invoices.append(account_move.id)

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
                        if rec.sale_line_id.tolerance_percentage:
                            tolerance_quantity = (product_uom_qty * rec.sale_line_id.tolerance_percentage) / 100
                        else:
                            tolerance_quantity = product_uom_qty
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
