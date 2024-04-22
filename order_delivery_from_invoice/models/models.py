from odoo import models, fields, api


class CustomAccountMove(models.Model):
    _inherit = 'account.move'

    def create_sales_order(self, invoice):
        # """Create, confirm a sales order, and link to the invoice."""
        sale_order = self.env['sale.order'].create({
            'partner_id': invoice.partner_id.id,
            'deal_ref': invoice.fusion_deal_ref,
            'incoterm': invoice.invoice_incoterm_id.id,
            'order_line': [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_uom_id.id,
                    'price_unit':  line.price_unit,
                }) for line in invoice.invoice_line_ids if line.product_id
            ],
        })
        sale_order.action_confirm()

        for invoice_line in invoice.invoice_line_ids:
            corresponding_sale_line = sale_order.order_line.filtered(
                lambda l: l.product_id == invoice_line.product_id and l.product_uom_qty == invoice_line.quantity)
            if corresponding_sale_line:
                invoice_line.sale_line_ids = [(6, 0, [corresponding_sale_line.id])]



        # invoice.sale_order_id = sale_order.id
        # invoice.invoice_origin = sale_order.name

        # Find and confirm the delivery order created by confirming the sales order
        delivery_order = self.env['stock.picking'].search([('sale_id', '=', sale_order.id)], limit=1)
        if delivery_order:
            delivery_order.move_ids.quantity_done = delivery_order.move_ids.product_qty
            delivery_order.action_assign()  # Optional: Checks availability of the products.
            delivery_order._action_done()  # Confirm the delivery order.
        # Optional: Link delivery order back to the invoice if needed. This would require a custom field on invoice.
        # invoice.write({'x_delivery_order_ids': [(4, delivery_order.id)]})
        return sale_order
    def create_purchase_order(self, invoice):
        """Create, confirm a purchase order, and link to the invoice."""
        for rec in self:
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', rec.company_id.id)],limit =1)
            purchase_order = self.env['purchase.order'].create({
                'partner_id': invoice.partner_id.id,
                'invoice_ids': [(4, invoice.id)],  # This line might need adjustment based on how you link purchase orders to invoices
                'partner_ref':invoice.fusion_reference,
                'order_line': [
                    (0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity,
                        'product_uom': line.product_uom_id.id,
                        'price_unit': line.price_unit,
                        'sh_warehouse_id': warehouse.id # Required field for purchase order lines
                    }) for line in invoice.invoice_line_ids if line.product_id
                ],
            })
            # purchase_order.button_confirm()

            for invoice_line in invoice.invoice_line_ids:
                corresponding_purchase_line = purchase_order.order_line.filtered(
                    lambda l: l.product_id == invoice_line.product_id and l.product_uom_qty == invoice_line.quantity)
                if corresponding_purchase_line:
                    invoice_line.purchase_line_id = corresponding_purchase_line

            delivery_order = self.env['stock.picking'].search([('purchase_id', '=', purchase_order.id)], limit=1)
            if delivery_order:
                delivery_order.move_ids.quantity_done = delivery_order.move_ids.product_qty
                delivery_order.action_assign()  # Optional: Checks availability of the products.
                delivery_order._action_done()  # Confirm the delivery order.

            return purchase_order

    def action_post(self):
        res = super(CustomAccountMove, self).action_post()
        for invoice in self:
            # Check conditions here (e.g., only for specific types of invoices)
            if invoice.move_type == 'out_invoice':
                self.create_sales_order(invoice)
            elif invoice.move_type == 'in_invoice':
                self.create_purchase_order(invoice)
        return res
