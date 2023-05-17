from odoo import fields, models, api


class TransferFields(models.Model):
    _inherit = 'stock.picking'

    rate = fields.Float('Rate', digits=(6, 3))
    transport_tolerance = fields.Float('Transport Tolerance', digits=(6, 3))
    nominated_total = fields.Float(compute='_compute_nominated_total', string='Truck Total Nominated', digits=(6, 3))
    loaded_total = fields.Float(compute='_compute_loaded_total', string='Truck Total Loaded', digits=(6, 3))
    offloaded_total = fields.Float(compute='_compute_offloaded_total', string='Truck Total Offloaded', digits=(6, 3))

    @api.depends('truck_transport_details_ids.nominated')
    def _compute_nominated_total(self):
        for picking in self:
            nominated_total = sum(picking.truck_transport_details_ids.mapped('nominated'))
            picking.nominated_total = nominated_total

    @api.depends('truck_transport_details_ids.loaded')
    def _compute_loaded_total(self):
        for picking in self:
            loaded_total = sum(picking.truck_transport_details_ids.mapped('loaded'))
            picking.loaded_total = loaded_total

    @api.depends('truck_transport_details_ids.offloaded')
    def _compute_offloaded_total(self):
        for picking in self:
            offloaded_total = sum(picking.truck_transport_details_ids.mapped('offloaded'))
            picking.offloaded_total = offloaded_total


