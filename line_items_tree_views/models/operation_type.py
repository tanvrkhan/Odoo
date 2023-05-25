from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_done_internal_transfer = fields.Float(string='Internal Transfer', compute='_compute_qty_done_internal_transfer',
                                              digits=(6, 3))
    qty_done_incoming=fields.Float("Incoming-dep")
    qty_done_outgoing=fields.Float("Outgoing-dep")

    qty_done_success = fields.Float(
        string='Incoming',
        compute='_compute_qty_done_success',
        store=True,
        help='Field displaying the quantity for the Success condition.'
    )
    qty_done_danger = fields.Float(
        string='Outgoing',
        store=True,
        compute='_compute_qty_done_danger',
        help='Field displaying the quantity for the Danger condition.'
    )
    qty_done_difference = fields.Float(
        string='Difference',
        compute='_compute_qty_difference',
        group_operator='sum',
    )

    @api.depends('qty_done', 'location_usage', 'location_dest_usage')
    def _compute_qty_done_danger(self):
        for record in self:
            if (record.location_usage in ['internal', 'transit']) and (
                    record.location_dest_usage not in ['internal', 'transit']):
                record.qty_done_danger = record.qty_done
                record.qty_done_success = 0.0
            else:
                record.qty_done_danger = 0.0
                record.qty_done_success = 0.0
    @api.depends('qty_done', 'location_usage', 'location_dest_usage')
    def _compute_qty_done_success(self):
        for record in self:
            if (record.location_usage not in ['internal', 'transit']) and (
                    record.location_dest_usage in ['internal', 'transit']):
                record.qty_done_danger = 0.0
                record.qty_done_success = record.qty_done
            else:
                record.qty_done_danger = 0.0
                record.qty_done_success = 0.0


    @api.depends('qty_done_success', 'qty_done_danger')
    def _compute_qty_difference(self):
        for record in self:
            if (record.location_usage not in ['internal', 'transit']) and (
                record.location_dest_usage in ['internal', 'transit']):
                record.qty_done_difference = record.qty_done
            else:
                record.qty_done_difference = record.qty_done*-1


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(StockMoveLine, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        for res in result:
            if '__domain' in res:
                lines = self.search(res['__domain'])
                total_qty_done_difference=0
                total_qty_done_success=0
                total_qty_done_danger=0
                for record in lines:
                    total_qty_done_difference += record.qty_done_difference
                    if (record.location_usage not in ['internal', 'transit']) and (
                            record.location_dest_usage in ['internal', 'transit']):
                        total_qty_done_success += record.qty_done_success
                    else:
                        total_qty_done_danger += record.qty_done_danger
                res['qty_done_difference'] = total_qty_done_difference
                res['qty_done_success'] = total_qty_done_success
                res['qty_done_danger'] = total_qty_done_danger
        return result

    @api.depends('qty_done', 'picking_type_id.code')
    def _compute_qty_done_internal_transfer(self):
        for record in self:
            if record.picking_type_id.code == 'internal':
                record.qty_done_internal_transfer = record.qty_done
            else:
                record.qty_done_internal_transfer = 0.0
