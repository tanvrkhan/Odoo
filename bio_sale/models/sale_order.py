# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('warehouse_id')
    def onchange_warehouse(self):
        self.origin_state_id = self.warehouse_id.partner_id.state_id.id
        self.origin_country_id = self.warehouse_id.partner_id.country_id.id
    origin_country_id = fields.Many2one('res.country', 'Origin Place')
    origin_state_id = fields.Many2one('res.country.state')
    business_uom_id = fields.Many2one('uom.uom', 'Business Unit', domain=lambda self: [('is_business', '=', True)],
                                      context={'default_is_business': True, 'default_uom_type': 'smaller'})

    financial_conditions = fields.Selection(
        [('prepaid', 'Prepaid'), ('opencr', 'Open Cr'), ('sblc', 'SBLC')])
    laycan_from = fields.Date()
    laycan_to = fields.Date()
    certificate_id = fields.Many2one('sale.certificate')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.picking_ids.write({
                'origin_country_id': order.origin_country_id.id,
                'origin_state_id': order.origin_state_id.id,
                'laycan_from': order.laycan_from,
                'laycan_to': order.laycan_to,
                'financial_conditions': order.financial_conditions,
                'business_uom_id': (
                    order.business_uom_id and order.business_uom_id.id) or False,
                })
        return res
