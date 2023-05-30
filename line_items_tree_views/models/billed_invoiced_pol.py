from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_to_billed = fields.Float(
        string='To Receive',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_to_billed',
        store=True
    )
    qty_to_invoiced_pol = fields.Float(
        string='To Invoice',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_to_invoice',
        store=True
    )

    @api.depends('product_qty', 'qty_received')
    def _compute_to_billed(self):
        for line in self:
            line.qty_to_billed = line.product_qty - line.qty_received

    @api.depends('product_uom_qty', 'qty_received', 'qty_invoiced', 'product_id.product_tmpl_id.detailed_type')
    def _compute_to_invoice(self):
        for line in self:
            product_type = line.product_id.product_tmpl_id.detailed_type
            if product_type == 'service':
                line.qty_to_invoiced_pol = line.product_uom_qty - line.qty_invoiced
            elif product_type == 'consu':
                line.qty_to_invoiced_pol = line.product_uom_qty - line.qty_invoiced
            elif product_type == 'product':
                line.qty_to_invoiced_pol = line.qty_received - line.qty_invoiced
            else:
                line.qty_to_invoiced_pol = 0.0
