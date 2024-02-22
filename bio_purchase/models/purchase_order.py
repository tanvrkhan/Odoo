# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    origin_country_id = fields.Many2one('res.country', 'Origin Place')
    origin_state_id = fields.Many2one('res.country.state')
    destination_partner_id = fields.Many2one('res.partner', 'Destination place')
    business_uom_id = fields.Many2one('uom.uom', 'Business Unit', domain=[('is_business', '=', True)],
                                      context={'default_is_business': True, 'default_uom_type': 'smaller'})
    financial_conditions = fields.Selection(
        [('prepaid', 'Prepaid'), ('opencr', 'Open Cr'), ('sblc', 'SBLC')])
    laycan_from = fields.Date()
    laycan_to = fields.Date()

    def _prepare_picking(self):
        values = super(PurchaseOrder, self)._prepare_picking()
        values.update({
            'origin_country_id': self.origin_country_id.id,
            'origin_state_id': self.origin_state_id.id,
            'destination_partner_id': self.destination_partner_id.id,
            'laycan_from': self.laycan_from,
            'laycan_to': self.laycan_to,
            'financial_conditions': self.financial_conditions,
            'business_uom_id': (
                self.business_uom_id and self.business_uom_id.id) or False,
            })
        return values
