# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    origin_country_id = fields.Many2one('res.country', 'Origin Place')
    origin_state_id = fields.Many2one('res.country.state')
    destination_partner_id = fields.Many2one('res.partner', 'Destination place', domain=[('parent_id', '!=', False)])
    business_uom_id = fields.Many2one('uom.uom', 'Business Unit', domain=lambda self: [('is_business', '=', True)],
                                      context={'default_is_business': True, 'default_uom_type': 'smaller'})
    financial_conditions = fields.Selection(
        [('prepaid', 'Prepaid'), ('opencr', 'Open Cr'), ('sblc', 'SBLC')])
    laycan_from = fields.Date()
    laycan_to = fields.Date()
