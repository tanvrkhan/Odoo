from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mt_volume = fields.Float('Volume (MT)', digits=(6, 3), compute='_compute_mt_volume', store=True)

    @api.depends('product_uom_qty', 'product_id.mt_factor')
    def _compute_mt_volume(self):
        for line in self:
            line.mt_volume = line.product_uom_qty * line.product_id.mt_factor
