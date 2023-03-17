# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.exceptions import UserError,Warning


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

    @api.onchange('consignee')
    def _domain_change(self):
        print('_domain_change_domain_change')
        domain = []
        if self.partner_id:
            if self.partner_id.child_ids:
                domain = self.partner_id.child_ids.ids
                domain.append(self.partner_id.id)
            else:
                domain.append(self.partner_id.id)
        print(domain,'domaindomain')
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
                        tolerance_quantity = (product_uom_qty*rec.sale_line_id.tolerance_percentage)/100
                        if rec.sale_line_id.tolerance_type == 'min_max':
                            if product_uom_qty + tolerance_quantity < rec.quantity_done or product_uom_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.sale_line_id.tolerance_type == 'max':
                            if product_uom_qty + tolerance_quantity < rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.sale_line_id.tolerance_type == 'min':
                            if product_uom_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                elif rec.purchase_line_id:
                    product_qty = rec.purchase_line_id.product_qty
                    if rec.purchase_line_id.tolerance_type:
                        tolerance_quantity = (product_qty * rec.purchase_line_id.tolerance_percentage) / 100
                        if rec.purchase_line_id.tolerance_type == 'min_max':
                            if product_qty + tolerance_quantity < rec.quantity_done or product_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.purchase_line_id.tolerance_type == 'max':
                            if product_qty + tolerance_quantity < rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.purchase_line_id.tolerance_type == 'min':
                            if product_qty - tolerance_quantity > rec.quantity_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
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
                        tolerance_quantity = (product_uom_qty*rec.move_id.sale_line_id.tolerance_percentage)/100
                        if rec.move_id.sale_line_id.tolerance_type == 'min_max':
                            if product_uom_qty + tolerance_quantity < rec.qty_done or product_uom_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.sale_line_id.tolerance_type == 'max':
                            if product_uom_qty + tolerance_quantity < rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.sale_line_id.tolerance_type == 'min':
                            if product_uom_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                elif rec.move_id.purchase_line_id:
                    product_qty = rec.move_id.purchase_line_id.product_qty
                    if rec.move_id.purchase_line_id.tolerance_type:
                        tolerance_quantity = (product_qty * rec.move_id.purchase_line_id.tolerance_percentage) / 100
                        if rec.move_id.purchase_line_id.tolerance_type == 'min_max':
                            if product_qty + tolerance_quantity < rec.qty_done or product_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.purchase_line_id.tolerance_type == 'max':
                            if product_qty + tolerance_quantity < rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
                        elif rec.move_id.purchase_line_id.tolerance_type == 'min':
                            if product_qty - tolerance_quantity > rec.qty_done:
                                return {'warning': {
                                    'title': _('Warning'),
                                    'message': _('Please note that the quantity is not within the tolerance limit of the order.')
                                }}
