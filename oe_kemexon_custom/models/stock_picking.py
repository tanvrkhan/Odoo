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
