# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    nomination_ids = fields.One2many(
        'bio.nomination', 'sale_id', string='Nomination')
    nomination_count = fields.Integer(compute='_compute_nomination_ids')

    @api.depends('nomination_ids')
    def _compute_nomination_ids(self):
        for order in self:
            order.nomination_count = len(order.nomination_ids)

    def action_view_nomination(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "bio.nomination",
            "domain": [('sale_id', '=', self.id)],
            "context": {"default_sale_id": self.id},
            "name": "Nominations",
            'view_mode': 'tree,form',
        }
        if self.nomination_count == 1:
            result['view_mode'] = 'form'
            result['res_id'] = self.nomination_ids.id
        return result
