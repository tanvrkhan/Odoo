from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_done_incoming = fields.Float(string='Incoming', compute='_compute_qty_done_incoming', digits=(6, 3))
    qty_done_outgoing = fields.Float(string='Outgoing', compute='_compute_qty_done_outgoing', digits=(6, 3))
    qty_done_internal_transfer = fields.Float(string='Internal Transfer', compute='_compute_qty_done_internal_transfer', digits=(6, 3))

    @api.depends('qty_done', 'picking_type_id.code')
    def _compute_qty_done_incoming(self):
        for record in self:
            if record.picking_type_id.code == 'incoming':
                record.qty_done_incoming = record.qty_done
            else:
                record.qty_done_incoming = 0.0

    @api.depends('qty_done', 'picking_type_id.code')
    def _compute_qty_done_outgoing(self):
        for record in self:
            if record.picking_type_id.code == 'outgoing':
                record.qty_done_outgoing = record.qty_done
            else:
                record.qty_done_outgoing = 0.0

    @api.depends('qty_done', 'picking_type_id.code')
    def _compute_qty_done_internal_transfer(self):
        for record in self:
            if record.picking_type_id.code == 'internal':
                record.qty_done_internal_transfer = record.qty_done
            else:
                record.qty_done_internal_transfer = 0.0

