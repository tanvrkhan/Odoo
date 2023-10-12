from odoo import models, fields, api


class ProformaInvoiceLines(models.Model):
    _name = 'proforma.invoice.line'
    _description = 'Proforma Invoice Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    sale_order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')

    product_id = fields.Many2one(related='sale_order_line_id.product_id', string='Product Variant')
    product_template_id = fields.Many2one(related='sale_order_line_id.product_id.product_tmpl_id', string='Product',
                                          readonly=True)
    sale_order_name = fields.Char(related='sale_order_line_id.order_id.name', string='Sale Order Name')

    name = fields.Text(related='sale_order_line_id.name', string='Description')
    analytic_distribution = fields.Json(related='sale_order_line_id.analytic_distribution', string='Analytic')
    # compute='_compute_analytic_distribution_formatted'
    customer_lead = fields.Float(related='sale_order_line_id.customer_lead', string='Lead Time')
    product_uom_qty = fields.Float(related='sale_order_line_id.customer_lead', string="Quantity")
    pfi_product_uom_qty = fields.Float(
        string="Quantity",)
    display_type = fields.Selection(
        related='sale_order_line_id.display_type',
        string="Display Type",
        readonly=True,
    )
    product_packaging_id = fields.Many2one(related='sale_order_line_id.product_packaging_id', string='Packaging')
    product_packaging_qty = fields.Float(related='sale_order_line_id.product_packaging_qty',
                                         string="Packaging Quantity")
    tolerance_type = fields.Selection(related='sale_order_line_id.tolerance_type', string='Tolerance Type',
                                      readonly=True)
    tolerance_percentage = fields.Float(related='sale_order_line_id.tolerance_percentage',
                                        string='Tolerance Percentage')
    product_uom = fields.Many2one(related='sale_order_line_id.product_uom', string='UoM')
    is_formula_pricing = fields.Boolean(related='sale_order_line_id.is_formula_pricing', string='Is Formula Pricing')
    formula_price = fields.Float(related='sale_order_line_id.formula_price', staring='Formula Price')
    premium = fields.Float(related='sale_order_line_id.premium', string='Premium')
    formula_description = fields.Char(related='sale_order_line_id.formula_description', string='Formula Description',
                                      readonly=True)

    pfi_price_unit = fields.Float(string='Unit Price', compute='_compute_pfi_price_unit', store=True, readonly=False)
    tax_id = fields.Many2many(related='sale_order_line_id.tax_id', string='Taxes')
    purchase_price = fields.Float(related='sale_order_line_id.purchase_price', string='Cost')
    margin = fields.Float(related='sale_order_line_id.margin', string='Margin')
    margin_percent = fields.Float(related='sale_order_line_id.margin_percent', string='Margin(%)')
    price_subtotal = fields.Monetary(string='Amount', readonly=True, currency_field='currency_id',
                                     compute='_compute_amount')
    currency_id = fields.Many2one(related='sale_order_line_id.currency_id', string='Currency')
    order_id = fields.Many2one(related='sale_order_line_id.order_id', string='Order Reference')
    proforma_invoice_ids = fields.Many2one('proforma.invoice', string="Proforma Invoice Line")
    analytic_distribution_formatted = fields.Char(string='Analytic',
                                                  compute='_compute_analytic_distribution_formatted',
                                                  store=True)
    qty_invoiced = fields.Float(related='sale_order_line_id.qty_invoiced',
                                string="Invoiced Quantity")
    company_id = fields.Many2one(
        related='sale_order_line_id.company_id',
        store=True, index=True, precompute=True)
    pricelist_item_id = fields.Many2one(related='sale_order_line_id.pricelist_item_id', string='Pricelist Items')
    product_no_variant_attribute_value_ids = fields.Many2many(
        related='sale_order_line_id.product_no_variant_attribute_value_ids',
        string="Extra Values")
    is_downpayment = fields.Boolean(related='sale_order_line_id.is_downpayment',
                                    string="Is a down payment")
    discount = fields.Float(related='sale_order_line_id.discount',
                            string="Discount (%)")

    @api.depends('pfi_price_unit', 'pfi_product_uom_qty')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.pfi_price_unit * line.pfi_product_uom_qty

    @api.depends('product_id', 'product_uom', 'pfi_product_uom_qty', 'is_formula_pricing', 'premium', 'formula_price')
    def _compute_pfi_price_unit(self):
        for line in self:
            if line.is_formula_pricing:
                line.pfi_price_unit = line.formula_price + line.premium
            else:
                line.pfi_price_unit = 0

    @api.depends('pfi_price_unit', 'discount')
    def _compute_price_reduce(self):
        for line in self:
            line.price_reduce = line.pfi_price_unit * (1.0 - line.discount / 100.0)

    def _get_display_price(self):
        """Compute the displayed unit price for a given line.

        Overridden in custom flows:
        * where the price is not specified by the pricelist
        * where the discount is not specified by the pricelist

        Note: self.ensure_one()
        """
        self.ensure_one()

        pricelist_price = self._get_pricelist_price()

        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return pricelist_price

        if not self.pricelist_item_id:
            # No pricelist rule found => no discount from pricelist
            return pricelist_price

        base_price = self._get_pricelist_price_before_discount()

        # negative discounts (= surcharge) are included in the display price
        return max(base_price, pricelist_price)

    @api.depends('analytic_distribution')
    def _compute_analytic_distribution_formatted(self):
        for record in self:
            analytic_distribution = record.analytic_distribution
            if analytic_distribution:
                formatted = []
                for account_id in analytic_distribution:
                    accounts = self.env['account.analytic.account'].search([('id', '=', account_id)])
                    account_names = [account.name for account in accounts]
                    formatted.extend(account_names)
                record.analytic_distribution_formatted = ', '.join(formatted)
            else:
                record.analytic_distribution_formatted = ''

