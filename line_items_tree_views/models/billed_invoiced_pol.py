from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_to_billed = fields.Float(
        string='To Receive',
        digits=(6, 3),  # set 6 as the total number of digits and 3 as the number of decimal places
        compute='_compute_to_billed',

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

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(PurchaseOrderLine, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        for res in result:
            if '__domain' in res:
                lines = self.search(res['__domain'])
                total_qty_to_billed = 0
                total_product_qty = 0
                total_qty_received = 0
                for line in lines:
                    line.qty_to_billed = line.product_qty - line.qty_received

                res['qty_to_billed'] = total_qty_to_billed
                res['product_qty'] = total_product_qty
                res['qty_received'] = total_qty_received
        return result

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


