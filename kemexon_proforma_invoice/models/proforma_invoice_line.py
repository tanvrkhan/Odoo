from odoo import models, fields
from odoo.odoo import api
from odoo.tools import float_is_zero, float_compare, float_round


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

    # @api.depends('display_type', 'product_id', 'product_packaging_qty')
    # def _compute_pfi_product_uom_qty(self):
    #     for line in self:
    #         if line.display_type:
    #             line.pfi_product_uom_qty = 0.0
    #             continue
    #
    #         if not line.product_packaging_id:
    #             continue
    #         packaging_uom = line.product_packaging_id.product_uom_id
    #         qty_per_packaging = line.product_packaging_id.qty
    #         pfi_product_uom_qty = packaging_uom._compute_quantity(
    #             line.product_packaging_qty * qty_per_packaging, line.product_uom)
    #         if float_compare(pfi_product_uom_qty, line.pfi_product_uom_qty, precision_rounding=line.product_uom.rounding) != 0:
    #             line.pfi_product_uom_qty = pfi_product_uom_qty

    @api.depends('pfi_price_unit', 'pfi_product_uom_qty')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.pfi_price_unit * line.pfi_product_uom_qty

    # @api.depends('product_id', 'product_uom', 'pfi_product_uom_qty')
    # def _compute_pricelist_item_id(self):
    #     for line in self:
    #         if not line.product_id or line.display_type or not line.order_id.pricelist_id:
    #             line.pricelist_item_id = False
    #         else:
    #             line.pricelist_item_id = line.order_id.pricelist_id._get_product_rule(
    #                 line.product_id,
    #                 line.pfi_product_uom_qty or 1.0,
    #                 uom=line.product_uom,
    #                 date=line.order_id.date_order,
    #             )

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

    # def _convert_to_tax_base_line_dict(self):
    #     """ Convert the current record to a dictionary in order to use the generic taxes computation method
    #     defined on account.tax.
    #
    #     :return: A python dictionary.
    #     """
    #     self.ensure_one()
    #     return self.env['account.tax']._convert_to_tax_base_line_dict(
    #         self,
    #         partner=self.order_id.partner_id,
    #         currency=self.order_id.currency_id,
    #         product=self.product_id,
    #         taxes=self.tax_id,
    #         pfi_price_unit=self.pfi_price_unit,
    #         quantity=self.pfi_product_uom_qty,
    #         discount=self.discount,
    #         price_subtotal=self.price_subtotal,
    #     )

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

    # def _get_pricelist_price(self):
    #     """Compute the price given by the pricelist for the given line information.
    #
    #     :return: the product sales price in the order currency (without taxes)
    #     :rtype: float
    #     """
    #     self.ensure_one()
    #     self.product_id.ensure_one()
    #
    #     pricelist_rule = self.pricelist_item_id
    #     order_date = self.order_id.date_order or fields.Date.today()
    #     product = self.product_id.with_context(**self._get_product_price_context())
    #     qty = self.pfi_product_uom_qty or 1.0
    #     uom = self.product_uom or self.product_id.uom_id
    #
    #     price = pricelist_rule._compute_price(
    #         product, qty, uom, order_date, currency=self.currency_id)
    #
    #     return price



    # def _get_pricelist_price_before_discount(self):
    #     """Compute the price used as base for the pricelist price computation.
    #
    #     :return: the product sales price in the order currency (without taxes)
    #     :rtype: float
    #     """
    #     self.ensure_one()
    #     self.product_id.ensure_one()
    #
    #     pricelist_rule = self.pricelist_item_id
    #     order_date = self.order_id.date_order or fields.Date.today()
    #     product = self.product_id.with_context(**self._get_product_price_context())
    #     qty = self.pfi_product_uom_qty or 1.0
    #     uom = self.product_uom
    #
    #     if pricelist_rule:
    #         pricelist_item = pricelist_rule
    #         if pricelist_item.pricelist_id.discount_policy == 'without_discount':
    #             # Find the lowest pricelist rule whose pricelist is configured
    #             # to show the discount to the customer.
    #             while pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id.discount_policy == 'without_discount':
    #                 rule_id = pricelist_item.base_pricelist_id._get_product_rule(
    #                     product, qty, uom=uom, date=order_date)
    #                 pricelist_item = self.env['product.pricelist.item'].browse(rule_id)
    #
    #         pricelist_rule = pricelist_item
    #
    #     price = pricelist_rule._compute_base_price(
    #         product,
    #         qty,
    #         uom,
    #         order_date,
    #         target_currency=self.currency_id,
    #     )
    #
    #     return price

    # @api.depends('product_id', 'product_uom', 'pfi_product_uom_qty')
    # def _compute_discount(self):
    #     for line in self:
    #         if not line.product_id or line.display_type:
    #             line.discount = 0.0
    #
    #         if not (
    #                 line.order_id.pricelist_id
    #                 and line.order_id.pricelist_id.discount_policy == 'without_discount'
    #         ):
    #             continue
    #
    #         line.discount = 0.0
    #
    #         if not line.pricelist_item_id:
    #             # No pricelist rule was found for the product
    #             # therefore, the pricelist didn't apply any discount/change
    #             # to the existing sales price.
    #             continue
    #
    #         line = line.with_company(line.company_id)
    #         pricelist_price = line._get_pricelist_price()
    #         base_price = line._get_pricelist_price_before_discount()
    #
    #         if base_price != 0:  # Avoid division by zero
    #             discount = (base_price - pricelist_price) / base_price * 100
    #             if (discount > 0 and base_price > 0) or (discount < 0 and base_price < 0):
    #                 # only show negative discounts if price is negative
    #                 # otherwise it's a surcharge which shouldn't be shown to the customer
    #                 line.discount = discount


    # def _get_product_price_context(self):
    #     """Gives the context for product price computation.
    #
    #     :return: additional context to consider extra prices from attributes in the base product price.
    #     :rtype: dict
    #     """
    #     self.ensure_one()
    #     res = {}
    #
    #     # It is possible that a no_variant attribute is still in a variant if
    #     # the type of the attribute has been changed after creation.
    #     no_variant_attributes_price_extra = [
    #         ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
    #             lambda ptav:
    #                 ptav.price_extra and
    #                 ptav not in self.product_id.product_template_attribute_value_ids
    #         )
    #     ]
    #     if no_variant_attributes_price_extra:
    #         res['no_variant_attributes_price_extra'] = tuple(no_variant_attributes_price_extra)
    #
    #     return res
    #

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

