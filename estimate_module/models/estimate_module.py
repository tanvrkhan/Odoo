# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EstimateModule(models.Model):
    _name = 'estimate.module'
    _description = 'Estimate Module'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Name', store=True, tracking=True,  readonly=True, default=lambda self: _('New'))

    ## for purchase table
    purchase_line_ids = fields.One2many('estimate.purchase.line', 'estimate_module_id',
                                        string='Purchase Line IDS')

    ## for sales table
    sale_line_ids = fields.One2many('estimate.sale.line', 'estimate_module_id',
                                        string='Sale Line IDS')

    ## for costs table
    cost_line_ids = fields.One2many('estimate.cost.line', 'estimate_module_id',
                                    string='Cost Line IDS')

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

    ## for total qty
    total_purchase_budgeted_qty = fields.Float(string='Total Purchase Budgeted Qty.', store=True, tracking=True, compute='get_total_purchase_qty')
    total_purchase_confirmed_qty = fields.Float(string='Total Purchase Confirmed Qty.', store=True, tracking=True, compute='get_total_purchase_qty')
    total_purchase_realized_qty = fields.Float(string='Total Purchase Realized Qty.', store=True, tracking=True, compute='get_total_purchase_qty')

    total_sale_budgeted_qty = fields.Float(string='Total Sale Budgeted Qty.', store=True, tracking=True,
                                               compute='get_total_sale_qty')
    total_sale_confirmed_qty = fields.Float(string='Total Sale Confirmed Qty.', store=True, tracking=True,
                                                compute='get_total_sale_qty')
    total_sale_realized_qty = fields.Float(string='Total Sale Realized Qty.', store=True, tracking=True,
                                                compute='get_total_sale_qty')

    total_budgeted_qty = fields.Float(string='Total Budgeted Qty', store=True, tracking=True, compute='get_total_qty')
    total_confirmed_qty = fields.Float(string='Total Confirmed Qty', store=True, tracking=True, compute='get_total_qty')
    total_realized_qty = fields.Float(string='Total Realized Qty', store=True, tracking=True, compute='get_total_qty')

    @api.depends('purchase_line_ids.quantity')
    def get_total_purchase_qty(self):
        purchase_budgeted_qty = 0
        purchase_confirmed_qty = 0
        for rec in self:
            if rec.purchase_line_ids:
                # if rec.total_purchase_budgeted_qty > 0:
                #     purchase_budgeted_qty = rec.total_purchase_budgeted_qty
                # else:
                # purchase_budgeted_qty = 0
                if rec.total_purchase_confirmed_qty > 0:
                    purchase_confirmed_qty = rec.total_purchase_confirmed_qty
                else:
                    purchase_confirmed_qty = 0
                if rec.total_purchase_realized_qty > 0:
                    purchase_realized_qty = rec.total_purchase_realized_qty
                else:
                    purchase_realized_qty = 0
                for purchase in rec.purchase_line_ids:
                    # if purchase.qty_confirmed == True:
                    #     purchase_confirmed_qty += purchase.quantity
                    purchase_budgeted_qty += purchase.quantity
                rec.total_purchase_budgeted_qty = purchase_budgeted_qty
                rec.total_purchase_confirmed_qty = purchase_confirmed_qty
                rec.total_purchase_realized_qty = purchase_realized_qty

    @api.depends('sale_line_ids.quantity')
    def get_total_sale_qty(self):
        sale_budgeted_qty = 0
        sale_confirmed_qty = 0
        for rec in self:
            if rec.sale_line_ids:
                # if rec.total_sale_budgeted_qty > 0:
                #     sale_budgeted_qty = rec.total_sale_budgeted_qty
                # else:
                #     sale_budgeted_qty = 0
                if rec.total_sale_confirmed_qty > 0:
                    sale_confirmed_qty = rec.total_sale_confirmed_qty
                else:
                    sale_confirmed_qty = 0
                if rec.total_sale_realized_qty > 0:
                    sale_realized_qty = rec.total_sale_realized_qty
                else:
                    sale_realized_qty = 0
                for sale in rec.sale_line_ids:
                    # if sale.qty_confirmed == True:
                    #     sale_confirmed_qty += sale.quantity
                    sale_budgeted_qty += sale.quantity
                rec.total_sale_budgeted_qty = sale_budgeted_qty
                rec.total_sale_confirmed_qty = sale_confirmed_qty
                rec.total_sale_realized_qty = sale_realized_qty

    @api.depends('total_purchase_budgeted_qty', 'total_sale_budgeted_qty',
                 'total_purchase_confirmed_qty', 'total_sale_confirmed_qty',
                 'total_purchase_realized_qty', 'total_sale_realized_qty')
    def get_total_qty(self):
        for rec in self:
            rec.total_budgeted_qty = rec.total_purchase_budgeted_qty + rec.total_sale_budgeted_qty
            rec.total_confirmed_qty = rec.total_purchase_confirmed_qty + rec.total_sale_confirmed_qty
            rec.total_realized_qty = rec.total_purchase_realized_qty + rec.total_sale_realized_qty
    ## for total qty

    # total purchases
    total_budgeted_purchases = fields.Float(string='Total Budgeted Purchases', store=True, tracking=True,
                                               compute='get_total_purchases')
    total_confirmed_purchases = fields.Float(string='Total Confirmed Purchases', store=True, tracking=True,
                                                compute='get_total_purchases')
    total_realized_purchases = fields.Float(string='Total Realized Purchases', store=True, tracking=True,
                                                compute='get_total_purchases')

    @api.depends('purchase_line_ids.base_amount')
    def get_total_purchases(self):
        for rec in self:
            total_budgeted_purchase_price = 0
            if rec.total_confirmed_purchases > 0:
                total_confirmed_purchase_price = rec.total_confirmed_purchases
            else:
                total_confirmed_purchase_price = 0
            if rec.total_realized_purchases > 0:
                total_realized_purchase_price = rec.total_realized_purchases
            else:
                total_realized_purchase_price = 0
            if rec.purchase_line_ids:
                for purchase in rec.purchase_line_ids:
                    # if purchase.price_confirmed == True:
                    #     total_confirmed_purchase_price += purchase.base_amount
                    total_budgeted_purchase_price += purchase.base_amount
                rec.total_budgeted_purchases = (total_budgeted_purchase_price)
                rec.total_confirmed_purchases = (total_confirmed_purchase_price)
                rec.total_realized_purchases = (total_realized_purchase_price)
    # total purchases

    # total sales
    total_budgeted_sales = fields.Float(string='Total Budgeted Sales', store=True, tracking=True,
                                            compute='get_total_sales')
    total_confirmed_sales = fields.Float(string='Total Confirmed Sales', store=True, tracking=True,
                                             compute='get_total_sales')
    total_realized_sales = fields.Float(string='Total Realized Sales', store=True, tracking=True,
                                         compute='get_total_sales')

    @api.depends('sale_line_ids.base_amount')
    def get_total_sales(self):
        for rec in self:
            total_budgeted_sale_price = 0
            if rec.total_confirmed_sales > 0:
                total_confirmed_sale_price = rec.total_confirmed_sales
            else:
                total_confirmed_sale_price = 0
            if rec.total_realized_sales > 0:
                total_realized_sale_price = rec.total_realized_sales
            else:
                total_realized_sale_price = 0
            if rec.sale_line_ids:
                for sale in rec.sale_line_ids:
                    # if sale.price_confirmed == True:
                    #     total_confirmed_sale_price += sale.base_amount
                    total_budgeted_sale_price += sale.base_amount
                rec.total_budgeted_sales = (total_budgeted_sale_price)
                rec.total_confirmed_sales = (total_confirmed_sale_price)
                rec.total_realized_sales = (total_realized_sale_price)
    # total sales

    # total costs
    total_budgeted_costs = fields.Float(string='Total Budgeted Costs', store=True, tracking=True,
                                        compute='get_total_costs')
    total_confirmed_costs = fields.Float(string='Total Confirmed Costs', store=True, tracking=True,
                                         compute='get_total_costs')
    total_realized_costs = fields.Float(string='Total Realized Costs', store=True, tracking=True,
                                         compute='get_total_costs')

    @api.depends('cost_line_ids.base_amount')
    def get_total_costs(self):
        for rec in self:
            total_budgeted_cost_price = 0
            if rec.total_confirmed_costs > 0:
                total_confirmed_cost_price = rec.total_confirmed_costs
            else:
                total_confirmed_cost_price = 0
            if rec.total_realized_costs > 0:
                total_realized_cost_price = rec.total_realized_costs
            else:
                total_realized_cost_price = 0
            if rec.cost_line_ids:
                for cost in rec.cost_line_ids:
                    # total_confirmed_cost_price += cost.base_amount
                    if cost.our_share:
                        total_budgeted_cost_price += cost.our_share
                    else:
                        total_budgeted_cost_price += cost.base_amount
                rec.total_budgeted_costs = (total_budgeted_cost_price)
                rec.total_confirmed_costs = (total_confirmed_cost_price)
                rec.total_realized_costs = (total_realized_cost_price)
    # total costs

    # total margin
    total_budgeted_margin = fields.Float(string='Total Budgeted Margin', store=True, tracking=True,
                                        compute='get_total_margin')
    total_confirmed_margin = fields.Float(string='Total Confirmed Margin', store=True, tracking=True,
                                        compute='get_total_margin')
    total_realized_margin = fields.Float(string='Total Realized Margin', store=True, tracking=True,
                                        compute='get_total_margin')

    @api.depends('total_budgeted_purchases', 'total_budgeted_sales', 'total_budgeted_costs',
                 'total_confirmed_purchases', 'total_confirmed_sales', 'total_confirmed_costs',
                 'total_realized_purchases', 'total_realized_sales', 'total_realized_costs')
    def get_total_margin(self):
        for rec in self:
            rec.total_budgeted_margin = rec.total_budgeted_sales - rec.total_budgeted_purchases - rec.total_budgeted_costs
            rec.total_confirmed_margin = rec.total_confirmed_sales - rec.total_confirmed_purchases - rec.total_confirmed_costs
            rec.total_realized_margin = rec.total_realized_sales - rec.total_realized_purchases - rec.total_realized_costs
    # total margin

    # total per unit margin
    total_budgeted_unit_margin = fields.Float(string='Total Budgeted Per Unit Margin', store=True, tracking=True,
                                         compute='get_total_unit_margin')
    total_confirmed_unit_margin = fields.Float(string='Total Confirmed Per Unit Margin', store=True, tracking=True,
                                          compute='get_total_unit_margin')
    total_realized_unit_margin = fields.Float(string='Total Realized Per Unit Margin', store=True, tracking=True,
                                               compute='get_total_unit_margin')

    @api.depends('total_budgeted_qty', 'total_confirmed_qty',
                 'total_budgeted_margin', 'total_confirmed_margin',
                 'total_realized_margin', 'total_realized_qty')
    def get_total_unit_margin(self):
        for rec in self:
            if rec.total_budgeted_qty > 0:
                rec.total_budgeted_unit_margin = rec.total_budgeted_margin / rec.total_budgeted_qty
            if rec.total_confirmed_qty > 0:
                rec.total_confirmed_unit_margin = rec.total_confirmed_margin / rec.total_confirmed_qty
            if rec.total_realized_qty > 0:
                rec.total_realized_unit_margin = rec.total_realized_margin / rec.total_realized_qty
    # total per unit margin

    def validate_lines(self):
        for rec in self:
            sale_lines = rec.sale_line_ids
            purchase_lines = rec.purchase_line_ids
            total_sale_line_quantity = 0
            total_purchase_line_quantity = 0
            if sale_lines and purchase_lines:
                # create a dictionary to group sale lines by product
                sale_totals = {}
                for line in sale_lines:
                    if line.product_id in sale_totals:
                        sale_totals[line.product_id]['total_qty'] += line.quantity
                        sale_totals[line.product_id]['estimate_line_id'].append(line)
                    else:
                        sale_totals[line.product_id] = {'total_qty': line.quantity,
                                                        'estimate_line_id': [line]}

                # create a dictionary to group purchase lines by product
                purchase_totals = {}
                for line in purchase_lines:
                    if line.product_id in purchase_totals:
                        purchase_totals[line.product_id]['total_qty'] += line.quantity
                        purchase_totals[line.product_id]['estimate_line_id'].append(line)
                    else:
                        purchase_totals[line.product_id] = {'total_qty': line.quantity,
                                                            'estimate_line_id': [line]}

                # check for matching purchase and sale lines for each group
                for group_lines in purchase_totals.items():
                    matching_purchase_lines = group_lines[1]['estimate_line_id']
                    matching_sale_lines = sale_lines.filtered(
                        lambda l: l.product_id == group_lines[0])
                    group_quantity = sum(line.quantity for line in matching_purchase_lines)

                    for sale_line in matching_sale_lines:
                        sale_line_quantity = sale_line.quantity
                        total_sale_line_quantity = sum(line.quantity for line in matching_sale_lines)
                        if sale_line_quantity == group_quantity:
                            group_quantity -= sale_line_quantity
                            sale_line.validate_check = True
                        elif total_sale_line_quantity == group_quantity:
                            group_quantity = total_sale_line_quantity
                            sale_line.validate_check = True

                    # mark lines as validated
                    if group_quantity == 0:
                        for purchase_line in matching_purchase_lines:
                            purchase_line.validate_check = True
                    elif group_quantity == total_sale_line_quantity:
                        for purchase_line in matching_purchase_lines:
                            purchase_line.validate_check = True

                # check for matching purchase and sale lines for each group
                for group_lines in sale_totals.items():
                    matching_sale_lines = group_lines[1]['estimate_line_id']
                    matching_purchase_lines = purchase_lines.filtered(
                        lambda l: l.product_id == group_lines[0])
                    group_quantity = sum(line.quantity for line in matching_sale_lines)

                    for purchase_line in matching_purchase_lines:
                        purchase_line_quantity = purchase_line.quantity
                        total_purchase_line_quantity = sum(line.quantity for line in matching_purchase_lines)
                        if purchase_line_quantity == group_quantity:
                            group_quantity -= purchase_line_quantity
                            purchase_line.validate_check = True
                        elif total_purchase_line_quantity == group_quantity:
                            group_quantity = total_purchase_line_quantity
                            purchase_line.validate_check = True

                    # mark lines as validated
                    if group_quantity == 0:
                        for sale_line in matching_sale_lines:
                            sale_line.validate_check = True
                    elif group_quantity == total_purchase_line_quantity:
                        for sale_line in matching_sale_lines:
                            sale_line.validate_check = True

    analytic_account_id = fields.Many2one('account.analytic.account', store=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('estimate.module.sequence') or _('New')
        res = super(EstimateModule, self).create(vals)
        return res


class PurchaseLines(models.Model):
    _name = 'estimate.purchase.line'

    estimate_module_id = fields.Many2one('estimate.module', string='Estimate ID')
    seller_id = fields.Many2one('res.partner', string='Seller', store=True, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', store=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    delivery_location_id = fields.Many2one('stock.picking.type', domain="[('code','=','incoming'), '|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
                                           string='Delivery Loc.', store=True, tracking=True)
    lc_boolean = fields.Boolean(string='LC', store=True, tracking=True)
    quantity = fields.Float(string='Quantity', store=True, tracking=True)
    qty_confirmed = fields.Boolean(string='Qty Confirmed', store=True, tracking=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', string='UOM', store=True, tracking=True)
    price = fields.Float(string='Price', store=True, tracking=True)
    price_confirmed = fields.Boolean(string='Price Confirmed', store=True, tracking=True)
    base_amount = fields.Float(string='Base Amount', store=True, tracking=True, compute='calculate_base_amount')
    converted_amount = fields.Float(string='Converted Amount', store=True, tracking=True, compute='calculate_converted_amount')
    vessel_id = fields.Many2one('vessel.information', string='Vessel', store=True, tracking=True)
    deal_date = fields.Date(string='Deal Date', store=True, tracking=True)
    notes = fields.Char(string='Notes', store=True, tracking=True)
    due_date = fields.Date(string='Due Date', store=True, tracking=True)
    lc_amount = fields.Float(string='LC Amount', store=True, tracking=True)
    bank_id = fields.Many2one('res.bank', store=True, tracking=True)

    analytic_account_id = fields.Many2one('account.analytic.account', store=True, tracking=True,
                                          compute='get_default_analytic_account', readonly=False)

    @api.depends('estimate_module_id')
    def get_default_analytic_account(self):
        for rec in self:
            if rec.estimate_module_id:
                rec.analytic_account_id = rec.estimate_module_id.analytic_account_id.id

    vendor_reference = fields.Char(string='Vendor Ref.', store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', store=True, tracking=True,
                                  default=lambda self: self.env.company.currency_id)
    forex_rate = fields.Float(string='Forex Rate', store=True, tracking=True, compute='get_forex_rate')
    incoterms_id = fields.Many2one('account.incoterms', string='Incoterms', store=True, tracking=True)
    validate_check = fields.Boolean(string='Qty. Validated', store=True, tracking=True, readonly=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', store=True, tracking=True, readonly=True)

    @api.depends('currency_id')
    def get_forex_rate(self):
        for rec in self:
            if rec.currency_id:
                if rec.currency_id.name == 'USD':
                    rec.forex_rate = 1
                else:
                    rate = rec.currency_id.rate_ids.sorted(key=lambda r: r.name, reverse=True)
                    rec.forex_rate = rate[0].company_rate

    @api.depends('quantity', 'price')
    def calculate_base_amount(self):
        for rec in self:
            amount = rec.price * rec.quantity
            rec.base_amount = amount

    @api.depends('quantity', 'price', 'forex_rate')
    def calculate_converted_amount(self):
        for rec in self:
            amount = rec.price * rec.quantity
            rec.converted_amount = amount * rec.forex_rate

    def action_confirm_purchases(self):
        for rec in self:
            purchase_order_obj = self.env['purchase.order']
            if rec.qty_confirmed == False:
                raise ValidationError(_('Please check Qty Confirmed!'))
            if rec.validate_check == True and rec.qty_confirmed == True:
                vals = {
                    'partner_id': rec.seller_id.id,
                    'partner_ref': rec.vendor_reference,
                    'currency_id': rec.currency_id.id,
                    'picking_type_id': rec.delivery_location_id.id,
                    'incoterm_id': rec.incoterms_id.id,
                    'estimate_id': rec.estimate_module_id.id,
                    'estimate_purchase_line_id': rec.id
                }
                purchase_order = purchase_order_obj.search([('estimate_id', '=', rec.estimate_module_id.id),
                                                            ('estimate_purchase_line_id', '=', rec.id)])
                order_line_vals = {
                    'product_id': rec.product_id.id,
                    'name': rec.product_id.display_name,
                    'product_qty': rec.quantity,
                    'product_uom': rec.uom_id.id,
                    'price_unit': rec.price,
                    'price_subtotal': rec.base_amount,
                    'analytic_distribution': {rec.analytic_account_id.id: 100}
                }
                if purchase_order:
                        purchase_order.write(vals)
                        purchase_order.order_line.write(order_line_vals)
                else:
                    p = purchase_order_obj.create(vals)
                    rec.purchase_order_id = p.id
                    p.order_line = [(0, 0, order_line_vals)]
            else:
                raise ValidationError(_('The record should be validated first!'))


class SaleLines(models.Model):
    _name = 'estimate.sale.line'

    estimate_module_id = fields.Many2one('estimate.module', string='Estimate ID')
    buyer_id = fields.Many2one('res.partner', string='Buyer', store=True, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', store=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

    @api.depends('buyer_id')
    def get_warehouse_id(self):
        for rec in self:
            if rec.buyer_id.child_ids:
                for address in rec.buyer_id.child_ids:
                    if address.type == 'delivery':
                        rec.warehouse_id = address.warehouse_id.id
                    else:
                        rec.warehouse_id = self.env['stock.warehouse'].search([('name', '=', 'My Company')]).id
            else:
                rec.warehouse_id = self.env['stock.warehouse'].search([('name', '=', 'My Company')]).id

    warehouse_id = fields.Many2one('stock.warehouse', domain="[('company_id', 'in', [company_id, False])]",
                                           string='Warehouse', store=True, tracking=True, compute='get_warehouse_id')
    delivery_location_id = fields.Many2one('res.partner', domain="[('company_id', 'in', [company_id, False])]",
                                           string='Delivery Loc.', store=True, tracking=True, compute='_compute_buyer_shipping_id')

    @api.depends('buyer_id')
    def _compute_buyer_shipping_id(self):
        for rec in self:
            rec.delivery_location_id = rec.buyer_id.address_get(['delivery'])[
                'delivery'] if rec.buyer_id else False

    lc_boolean = fields.Boolean(string='LC', store=True, tracking=True)
    quantity = fields.Float(string='Quantity', store=True, tracking=True)
    qty_confirmed = fields.Boolean(string='Qty Confirmed', store=True, tracking=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', string='UOM', store=True, tracking=True)
    price = fields.Float(string='Price', store=True, tracking=True)
    price_confirmed = fields.Boolean(string='Price Confirmed', store=True, tracking=True)
    base_amount = fields.Float(string='Base Amount', store=True, tracking=True, compute='calculate_base_amount')
    converted_amount = fields.Float(string='Converted Amount', store=True, tracking=True, compute='calculate_converted_amount')
    vessel_id = fields.Many2one('vessel.information', string='Vessel', store=True, tracking=True)
    deal_date = fields.Date(string='Deal Date', store=True, tracking=True)
    notes = fields.Char(string='Notes', store=True, tracking=True)
    due_date = fields.Date(string='Due Date', store=True, tracking=True)
    lc_amount = fields.Float(string='LC Amount', store=True, tracking=True)
    bank_id = fields.Many2one('res.bank', store=True, tracking=True)
    analytic_account_id = fields.Many2one('account.analytic.account', store=True, tracking=True,
                                          compute='get_default_analytic_account', readonly=False)

    @api.depends('estimate_module_id')
    def get_default_analytic_account(self):
        for rec in self:
            if rec.estimate_module_id:
                rec.analytic_account_id = rec.estimate_module_id.analytic_account_id.id

    vendor_reference = fields.Char(string='Vendor Ref.', store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', store=True, tracking=True,
                                  default=lambda self: self.env.company.currency_id)
    forex_rate = fields.Float(string='Forex Rate', store=True, tracking=True, compute='get_forex_rate')
    incoterms_id = fields.Many2one('account.incoterms', string='Incoterms', store=True, tracking=True)
    validate_check = fields.Boolean(string='Qty. Validated', store=True, tracking=True, readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', store=True, tracking=True, readonly=True)

    @api.depends('currency_id')
    def get_forex_rate(self):
        for rec in self:
            if rec.currency_id:
                if rec.currency_id.name == 'USD':
                    rec.forex_rate = 1
                else:
                    rate = rec.currency_id.rate_ids.sorted(key=lambda r: r.name, reverse=True)
                    rec.forex_rate = rate[0].company_rate

    @api.depends('quantity', 'price', 'forex_rate')
    def calculate_converted_amount(self):
        for rec in self:
            amount = rec.price * rec.quantity
            rec.converted_amount = amount * rec.forex_rate

    @api.depends('quantity', 'price')
    def calculate_base_amount(self):
        for rec in self:
            amount = rec.price * rec.quantity
            rec.base_amount = amount

    def action_confirm_sales(self):
        for rec in self:
            sale_order_obj = self.env['sale.order']
            if rec.qty_confirmed == False:
                raise ValidationError(_('Please check Qty Confirmed!'))
            if rec.validate_check == True and rec.qty_confirmed == True:
                vals = {
                    'partner_id': rec.buyer_id.id,
                    'incoterm': rec.incoterms_id.id,
                    'warehouse_id': rec.warehouse_id.id,
                    'partner_shipping_id': rec.delivery_location_id.id,
                    'analytic_account_id': rec.analytic_account_id.id,
                    'deal_ref': rec.vendor_reference,
                    'estimate_id': rec.estimate_module_id.id,
                    'estimate_sale_line_id': rec.id
                }
                sale_order = sale_order_obj.search([('estimate_id', '=', rec.estimate_module_id.id),
                                                            ('estimate_sale_line_id', '=', rec.id)])

                order_line_vals = {
                    'product_id': rec.product_id.id,
                    'product_template_id': rec.product_id.product_tmpl_id.id,
                    'name': rec.product_id.display_name,
                    'product_uom_qty': rec.quantity,
                    'product_uom': rec.uom_id.id,
                    'price_unit': rec.price,
                    'customer_lead': 0.0,
                    'price_subtotal': rec.base_amount,
                    'analytic_distribution': {rec.analytic_account_id.id: 100}
                }
                if sale_order:
                    sale_order.write(vals)
                    sale_order.order_line.write(order_line_vals)
                else:
                    s = sale_order_obj.create(vals)
                    rec.sale_order_id = s.id
                    s.order_line = [(0, 0, order_line_vals)]
            else:
                raise ValidationError(_('The record should be validated first!'))

class CostLines(models.Model):
    _name = 'estimate.cost.line'

    estimate_module_id = fields.Many2one('estimate.module', string='Estimate ID')
    analytic_account_id = fields.Many2one('account.analytic.account', store=True, tracking=True,
                                          compute='get_default_analytic_account', readonly=False)

    @api.depends('estimate_module_id')
    def get_default_analytic_account(self):
        for rec in self:
            if rec.estimate_module_id:
                rec.analytic_account_id = rec.estimate_module_id.analytic_account_id.id

    product_id = fields.Many2one('product.product', string='Product', store=True, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', store=True, tracking=True)
    unit_price = fields.Float(string='Unit Price', store=True, tracking=True)
    quantity = fields.Float(string='Quantity', store=True, tracking=True)
    base_amount = fields.Float(string='Base Amount', store=True, tracking=True, compute='calculate_base_amount')
    converted_amount = fields.Float(string='Converted Amount', store=True, tracking=True, compute='calculate_converted_amount')
    currency_id = fields.Many2one('res.currency', store=True, tracking=True,
                                  default=lambda self: self.env.company.currency_id)
    forex_rate = fields.Float(string='Forex Rate', store=True, tracking=True, compute='get_forex_rate')
    debit_account_id = fields.Many2one('account.account', string='Debit Account',
                                               store=True, tracking=True,
                                       related='product_id.categ_id.property_account_income_categ_id')
    credit_account_id = fields.Many2one('account.account', string='Credit Account',
                                       store=True, tracking=True)
    journal_id = fields.Many2one('account.journal', string='Journal',
                                       store=True, tracking=True)
    counterparty = fields.Many2one('res.partner', string='Counterparty', store=True, tracking=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', string='UOM', store=True, tracking=True)
    our_percentage = fields.Integer(string='Our Percentage', store=True, tracking=True)
    our_share = fields.Float(string='Our Share', compute='get_our_share', store=True, tracking=True)
    account_move_id = fields.Many2one('account.move', string='Account Move', store=True, tracking=True, readonly=True)

    @api.depends('currency_id')
    def get_forex_rate(self):
        for rec in self:
            if rec.currency_id:
                if rec.currency_id.name == 'USD':
                    rec.forex_rate = 1
                else:
                    rate = rec.currency_id.rate_ids.sorted(key=lambda r: r.name, reverse=True)
                    rec.forex_rate = rate[0].company_rate

    @api.depends('quantity', 'unit_price', 'forex_rate')
    def calculate_converted_amount(self):
        for rec in self:
            amount = rec.unit_price * rec.quantity
            rec.converted_amount = amount * rec.forex_rate

    @api.depends('quantity', 'unit_price')
    def calculate_base_amount(self):
        for rec in self:
            amount = rec.unit_price * rec.quantity
            rec.base_amount = amount

    @api.depends('base_amount', 'our_percentage')
    def get_our_share(self):
        for rec in self:
            rec.our_share = rec.base_amount * (rec.our_percentage / 100)

    def action_confirm_costs(self):
        for rec in self:
            account_move_obj = self.env['account.move']
            amount_totals = {}
            ## if vendor selected, then create purchase bill
            if rec.vendor_id:
                vals = {
                    'partner_id': rec.vendor_id.id,
                    'journal_id': self.env['account.journal'].search([('name', '=', 'Purchases')]).id,
                    'estimate_id': rec.estimate_module_id.id,
                    'estimate_cost_line_id': rec.id,
                    'move_type': 'in_invoice'
                }
                account_move = account_move_obj.search([('estimate_id', '=', rec.estimate_module_id.id),
                                                    ('estimate_cost_line_id', '=', rec.id)])
                if rec.our_share:
                    order_line_vals = {
                        'product_id': rec.product_id.id,
                        'quantity': rec.quantity,
                        'product_uom_id': rec.uom_id.id,
                        'price_unit': rec.unit_price,
                        'discount': 100-rec.our_percentage,
                        'price_subtotal': rec.our_share,
                        'analytic_distribution': {rec.analytic_account_id.id: 100}
                    }
                else:
                    order_line_vals = {
                        'product_id': rec.product_id.id,
                        'quantity': rec.quantity,
                        'product_uom_id': rec.uom_id.id,
                        'price_unit': rec.unit_price,
                        'discount': rec.our_percentage,
                        'price_subtotal': rec.base_amount,
                        'analytic_distribution': {rec.analytic_account_id.id: 100}
                    }
                if account_move:
                    account_move.write(vals)
                    account_move.invoice_line_ids.write(order_line_vals)
                else:
                    a = account_move_obj.create(vals)
                    rec.account_move_id = a.id
                    a.invoice_line_ids = [(0, 0, order_line_vals)]
            ## else create journal entry
            else:
                ## get confirmed costs on journal entry
                total_costs = 0
                if rec.our_share:
                    total_costs = rec.our_share
                else:
                    total_costs = rec.base_amount
                if rec.estimate_module_id.total_confirmed_costs > 0:
                    rec.estimate_module_id.total_confirmed_costs += total_costs
                else:
                    rec.estimate_module_id.total_confirmed_costs = total_costs
                ## get confirmed costs on journal entry
                amount_totals[rec] = {'total_amount': rec.our_share if rec.our_share else rec.base_amount,
                                       'estimate_id': rec.estimate_module_id.id,
                                       'estimate_cost_line_id': rec.id,
                                       'debit_account_id': rec.debit_account_id.id,
                                       'credit_account_id': rec.credit_account_id.id,
                                       'journal_id': rec.journal_id.id,
                                       'partner_id': rec.vendor_id.id,
                                       'currency_id': rec.currency_id.id,
                                       'move_type': 'entry',
                                      'analytic_account_id': rec.analytic_account_id.id
                                       }

                for cost, data in amount_totals.items():
                    total_amount = data['total_amount']
                    estimate_id = data['estimate_id']
                    estimate_cost_line_id = data['estimate_cost_line_id']
                    debit_account_id = data['debit_account_id']
                    credit_account_id = data['credit_account_id']
                    journal_id = data['journal_id']
                    partner_id = data['partner_id']
                    currency_id = data['currency_id']
                    move_type = data['move_type']
                    analytic_account_id = data['analytic_account_id']
                    vals = {
                        'estimate_id': estimate_id,
                        'estimate_cost_line_id': estimate_cost_line_id,
                        'journal_id': journal_id,
                        'move_type': move_type
                    }

                    invoice_line_ids1 = {
                        'account_id': debit_account_id,
                        'partner_id': partner_id,
                        'currency_id': currency_id,
                        'debit': total_amount,
                        'credit': 0,
                        'analytic_distribution': {analytic_account_id: 100}
                    }

                    invoice_line_ids2 = {
                        'account_id': credit_account_id,
                        'partner_id': partner_id,
                        'currency_id': currency_id,
                        'debit': 0,
                        'credit': total_amount,
                        'analytic_distribution': {analytic_account_id: 100}
                    }

                    journal_entry = account_move_obj.search([('estimate_id', '=', rec.estimate_module_id.id),
                                                            ('estimate_cost_line_id', '=', rec.id)])
                    if journal_entry:
                        raise ValidationError(_('Cannot modify the record as journal entry has already been created'))
                    else:
                        j = account_move_obj.create(vals)
                        rec.account_move_id = j.id
                        j.invoice_line_ids = [(0, 0, invoice_line_ids1),
                                              (0,0, invoice_line_ids2)]

    @api.onchange('vendor_id')
    def get_vendor_credit_account(self):
        for rec in self:
            if rec.vendor_id:
                rec.credit_account_id = rec.vendor_id.property_account_payable_id.id