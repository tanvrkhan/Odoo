from odoo import models, fields, api


class ProformaInvoice(models.Model):
    _name = 'proforma.invoice'
    _description = 'Proforma Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    name = fields.Char(related='sale_order_id.name', string='Number', placeholder='New')
    partner_id = fields.Many2one(related='sale_order_id.partner_id', string='Customer')
    fi_lc_id = fields.Many2one(related='sale_order_id.fi_lc_id', string='Financial Instrument')
    analytic_accounts_summary = fields.Char(related='sale_order_id.analytic_accounts_summary',
                                            string='Analytic Accounts')
    incoterm = fields.Many2one(related='sale_order_id.incoterm', string='Incoterm')
    incoterm_location_custom = fields.Many2one(related='sale_order_id.incoterm_location_custom',
                                               string='Incoterm Location')
    status_custom = fields.Selection(related='sale_order_id.status_custom', string='Status')
    legal_entity = fields.Many2one(related='sale_order_id.legal_entity', string='Representing Entity')
    show_vat_ids = fields.Boolean(related='sale_order_id.show_vat_ids', string='Show VAT ID')
    en_plus = fields.Boolean(related='sale_order_id.en_plus', string='EN Plus')
    date_order = fields.Datetime(related='sale_order_id.date_order', string="Order Date")
    pfi_date = fields.Datetime(string='PFI Date')
    expected_date = fields.Datetime(related='sale_order_id.expected_date', string='Expected Date')
    amount_untaxed = fields.Monetary(related='sale_order_id.amount_untaxed', string='Untaxed Amount')
    amount_tax = fields.Monetary(related='sale_order_id.amount_tax', string='Taxes')
    amount_total = fields.Monetary(related='sale_order_id.amount_total', string='Total')
    pricelist_id = fields.Many2one(related='sale_order_id.pricelist_id', string='Pricelist')
    payment_term_id = fields.Many2one(related='sale_order_id.payment_term_id', string='Payment Terms')
    deal_ref = fields.Char(related='sale_order_id.deal_ref', string='Deal Ref')
    delivery_from = fields.Date(related='sale_order_id.delivery_from', string='Period')
    delivery_to = fields.Date(related='sale_order_id.delivery_to', string='To')
    delivery_status = fields.Selection(related='sale_order_id.delivery_status', string='Delivery Status')
    invoice_status = fields.Selection(related='sale_order_id.invoice_status', string='Invoice Status')
    tag_ids = fields.Many2many(related='sale_order_id.tag_ids', string='tags')
    state = fields.Selection(related='sale_order_id.state', string='Status')
    analytic_account_id = fields.Many2one(related='sale_order_id.analytic_account_id', string='Analytic Account')
    currency_id = fields.Many2one(related='sale_order_id.currency_id', string='Currency')
    effective_date = fields.Datetime(related='sale_order_id.effective_date', string='Effected Date')
    trader = fields.Many2one(related='sale_order_id.trader', string='Trader')
    team_id = fields.Many2one(related='sale_order_id.team_id', string='Sales Team')
    company_id = fields.Many2one(related='sale_order_id.company_id', string='Company')
    warehouse_id = fields.Many2one(related='sale_order_id.warehouse_id', string='Warehouse')
    show_formula_pricing = fields.Boolean(related='sale_order_id.show_formula_pricing', string='Show Formula Pricing')
    show_validity = fields.Boolean(related='sale_order_id.show_validity', string='Show Validity')
    valid_until = fields.Date(related='sale_order_id.valid_until', string='Valid Until')
    commitment_date = fields.Datetime(related='sale_order_id.commitment_date', string='Delivery Date')
    signed_by = fields.Char(related='sale_order_id.signed_by', string='Signed By')
    signed_on = fields.Datetime(related='sale_order_id.signed_on', string='Signed On')
    signature = fields.Binary(related='sale_order_id.signature', string='Signature', attachment=True)
    proforma_invoice_line_ids = fields.One2many("proforma.invoice.line", 'proforma_invoice_ids',
                                                 string="Proforma Invoice Lines",)
    notes = fields.Html(string='Notes')
    total_quantity = fields.Float(compute='_compute_total_quantity', string='Total Quantity')
    total_amount = fields.Monetary(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id')
    order_line = fields.One2many(related='sale_order_id.order_line', string="Order Line")
    show_hs_code = fields.Boolean('Show HS Code')

    @api.depends('proforma_invoice_line_ids.pfi_product_uom_qty')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.pfi_product_uom_qty for line in record.proforma_invoice_line_ids)

    @api.depends('proforma_invoice_line_ids.price_subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.price_subtotal for line in record.proforma_invoice_line_ids)

    def _get_order_lines_to_report(self):
        down_payment_lines = self.proforma_invoice_line_ids.filtered(lambda line:
            line.is_downpayment
            and not line.display_type
            and not line._get_downpayment_state()
        )

        def show_line(line):
            if not line.is_downpayment:
                return True
            elif line.display_type and down_payment_lines:
                return True  # Only show the down payment section if down payments were posted
            elif line in down_payment_lines:
                return True  # Only show posted down payments
            else:
                return False

        return self.proforma_invoice_line_ids.filtered(show_line)
