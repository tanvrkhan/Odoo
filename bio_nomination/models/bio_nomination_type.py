# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from ast import literal_eval
from odoo import models, fields


class BioNominationType(models.Model):
    _name = "bio.nomination.type"
    _description = "Nomination type"

    name = fields.Char('Nomination Type', required=True)
    code = fields.Selection(
        selection=[('trucks', 'Trucks'), ('vessels', 'Vessels'), ])

    def _get_action(self, action_xmlid):
        action = self.env["ir.actions.actions"]._for_xml_id(action_xmlid)
        if self:
            action['display_name'] = self.name

        context = {
            'search_default_nomination_type_id': [self.id],
            'default_nomination_type_id': self.id,
        }
        action_context = literal_eval(action['context'])
        context = {**action_context, **context}
        action['context'] = context
        return action

    def get_action_bio_nomination_sale_trucks_tree(self):
        return self._get_action(
            'bio_nomination.action_bio_nomination_for_sale_order_trucks')

    def get_action_bio_nomination_sale_vessels_tree(self):
        return self._get_action(
            'bio_nomination.action_bio_nomination_for_sale_order_vessels')

    def get_action_bio_nomination_purchase_trucks_tree(self):
        return self._get_action(
            'bio_nomination.action_bio_nomination_for_purchase_order_trucks')

    def get_action_bio_nomination_purchase_vessels_tree(self):
        return self._get_action(
            'bio_nomination.action_bio_nomination_for_purchase_order_vessels')
