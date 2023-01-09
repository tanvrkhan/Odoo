# -*- coding: utf-8 -*-
from odoo import fields, models, api


class InheritTruckTran(models.Model):
    _inherit = 'truck.transport.details'

    seq = fields.Char("Sequence")


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('truck_transport_details_ids')
    def _onchange_truck_transport(self):
        seq = 0
        for rec in self:
            for line in rec.truck_transport_details_ids:
                seq += 1
                line.seq = "0" + str(seq) if seq < 10 else str(seq)
