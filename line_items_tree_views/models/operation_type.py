from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_done_internal_transfer = fields.Float(string='Internal Transfer', compute='_compute_qty_done_internal_transfer',
                                              digits=(6, 3))
    qty_done_incoming=fields.Float("Incoming-dep")
    qty_done_outgoing=fields.Float("Outgoing-dep")

    qty_done_success = fields.Float(
        string='Incoming',
        related='qty_done',
        store=True,
        help='Field displaying the quantity for the Success condition.'
    )
    qty_done_danger = fields.Float(
        string='Outgoing',
        store=True,
        related='qty_done',
        help='Field displaying the quantity for the Danger condition.'
    )
    qty_done_difference = fields.Float(
        string='Difference',
        compute='_compute_qty_difference',
        group_operator='sum',
    )

    @api.depends('qty_done_success', 'qty_done_danger')
    def _compute_qty_difference(self):
        for record in self:
            record.qty_done_difference = record.qty_done_success - record.qty_done_danger

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(StockMoveLine, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        for res in result:
            if '__domain' in res:
                lines = self.search(res['__domain'])
                total_qty_done_difference = sum(lines.mapped('qty_done_difference'))
                res['qty_done_difference'] = total_qty_done_difference
                res['qty_done_difference'] = total_qty_success_difference
                res['qty_done_difference'] = total_qty_danger_difference
        return result

    @api.depends('qty_done', 'picking_type_id.code')
    def _compute_qty_done_internal_transfer(self):
        for record in self:
            if record.picking_type_id.code == 'internal':
                record.qty_done_internal_transfer = record.qty_done
            else:
                record.qty_done_internal_transfer = 0.0
