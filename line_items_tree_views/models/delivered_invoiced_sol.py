from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_to_delivered = fields.Float(
        string='To Deliver',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_to_delivered',
        store=True
    )

    qty_to_invoiced = fields.Float(
        string='To Invoice',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_to_invoiced',
        store=True
    )

    @api.depends('product_uom_qty', 'qty_delivered')
    def _compute_to_delivered(self):
        for line in self:
            line.qty_to_delivered = line.product_uom_qty - line.qty_delivered

    @api.depends('product_uom_qty', 'qty_delivered', 'qty_invoiced', 'product_id.product_tmpl_id.detailed_type')
    def _compute_to_invoiced(self):
        for line in self:
            product_type = line.product_id.product_tmpl_id.detailed_type
            if product_type == 'service':
                line.qty_to_invoiced = line.product_uom_qty - line.qty_invoiced
            elif product_type == 'consu':
                line.qty_to_invoiced = line.product_uom_qty - line.qty_invoiced
            elif product_type == 'product':
                line.qty_to_invoiced = line.qty_delivered - line.qty_invoiced
            else:
                line.qty_to_invoiced = 0.0


