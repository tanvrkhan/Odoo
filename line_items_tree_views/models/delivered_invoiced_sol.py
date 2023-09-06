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
    delivered_value = fields.Float(
        string='Delivered Value',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_delivered_value',
        store=True
    )
    invoiced_value = fields.Float(
        string='Invoiced Value',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_invoiced_value',
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

    @api.depends('price_unit', 'qty_delivered')
    def _compute_delivered_value(self):
        for line in self:
            line.delivered_value = line.price_unit * line.qty_delivered

    @api.depends('price_unit', 'qty_invoiced')
    def _compute_invoiced_value(self):
        for line in self:
            line.invoiced_value = line.price_unit * line.qty_invoiced



