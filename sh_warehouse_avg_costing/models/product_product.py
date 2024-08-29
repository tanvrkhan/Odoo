# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from odoo.tools import float_is_zero, float_repr


class ProductTmpl(models.Model):
    _inherit = "product.product"

    warehouse_cost_lines = fields.One2many('sh.warehouse.cost', 'product_id')

    def _stock_account_get_anglo_saxon_price_unit(self, uom=False, warehouse=False,date=False,quantity=False):
        # * Softhealer code Start *

        # Added warehouse in the argument and setting price based on warehouse

        # * Softhealer code end *

        price = 0.0
        if warehouse:
            price = self.get_price_from_valuations(warehouse,date,quantity)
            if not price:
                price =self.warehouse_cost_lines.filtered(
                    lambda x: x.warehouse_id.id == warehouse).cost
            if not price:
                price = self.standard_price
        else:
            price = self.get_price_from_valuations(warehouse,date,quantity)
            # price = self.standard_price
        if not self or not uom or self.uom_id.id == uom.id:
            return price or 0.0
        return self.uom_id._compute_price(price, uom)
    def get_price_from_valuations(self,warehouse,date=False,quantity=False):
        domain = [
            ('product_id', '=', self.product_variant_id.id),
            ('company_id', '=', self.env.company.id),
            ('stock_move_id.picking_id.date_done', '<=', date)
        ]
        if warehouse:
            domain.append(('warehouse_id', '=', warehouse.id))
        valuations = self.env['stock.valuation.layer'].read_group(
            domain=domain,
            fields=['warehouse_id', 'quantity', 'value'],
            # Fields to load
            groupby=['warehouse_id'],
            lazy=False  # Get results for each partner directly
        )
        quantity_left = sum(v['quantity'] for v in valuations)
        if quantity_left<quantity:
            domain.append(('quantity', '>', 0))
            valuations = self.env['stock.valuation.layer'].read_group(
                domain=domain,
                fields=['warehouse_id', 'quantity', 'value'],
                # Fields to load
                groupby=['warehouse_id'],
                lazy=False  # Get results for each partner directly
            )
        
        if valuations:
            if sum(v['quantity'] for v in valuations) > 0:
                return sum(v['value'] for v in valuations) / sum(v['quantity'] for v in valuations)
        
    def _prepare_out_svl_vals(self, quantity, company, warehouse=False,date=False):
        """Prepare the values for a stock valuation layer created by a delivery.

        :param quantity: the quantity to value, expressed in `self.uom_id`
        :return: values to use in a call to create
        :rtype: dict
        """
        # * Softhealer code Start *

        # Added warehouse in the argument, updated price according to warehouse
        # and passed the warehouse in the dict

        # * Softhealer code end *

        self.ensure_one()
        company_id = self.env.context.get('force_company', self.env.company.id)
        company = self.env['res.company'].browse(company_id)
        currency = company.currency_id
        # Quantity is negative for out valuation layers.
        quantity = -1 * quantity
        vals = {
            'product_id': self.id,
            'value': currency.round(quantity * self.standard_price),
            'unit_cost': self.standard_price,
            'quantity': quantity,
        }
        fifo_vals = self._run_fifo(abs(quantity), company)
        vals['remaining_qty'] = fifo_vals.get('remaining_qty')
        # In case of AVCO, fix rounding issue of standard price when needed.
        if self.cost_method == 'average':
            if warehouse:
                vals.update({
                    'warehouse_id': warehouse.id
                })
                price = self.warehouse_cost_lines.filtered(
                    lambda x: x.warehouse_id.id == warehouse.id).cost
                if price:                   
                    vals.update({
                        'value': quantity * price,
                        'unit_cost': price
                    })
                else:
                    price = self.get_price_from_valuations(warehouse,date,quantity)
                    if price:
                        vals.update({
                            'value': quantity * price,
                            'unit_cost': price
                        })
                    
            rounding_error = currency.round(self.standard_price * self.quantity_svl - self.value_svl)
            if rounding_error:
                # If it is bigger than the (smallest number of the currency * quantity) / 2,
                # then it isn't a rounding error but a stock valuation error, we shouldn't fix it under the hood ...
                if abs(rounding_error) <= (abs(quantity) * currency.rounding) / 2:
                    vals['value'] += rounding_error
                    vals['rounding_adjustment'] = '\nRounding Adjustment: %s%s %s' % (
                        '+' if rounding_error > 0 else '',
                        float_repr(rounding_error, precision_digits=currency.decimal_places),
                        currency.symbol
                    )
        if self.cost_method == 'fifo':
            vals.update(fifo_vals)       
        return vals

class ProductTemplate(models.Model):
    _inherit = "product.template"

    warehouse_cost_lines = fields.One2many('sh.warehouse.cost', 'product_id',related="product_variant_id.warehouse_cost_lines")
    
    def update_wh_costing(self):
        for rec in self:
            valuations = self.env['stock.valuation.layer'].read_group(
                domain=[('product_id', '=', rec.product_variant_id.id),
                        ('company_id', '=', self.env.company.id)
                       ],
                fields=['warehouse_id', 'quantity', 'value'],
                # Fields to load
                groupby=['warehouse_id'],
                lazy=False  # Get results for each partner directly
            )
            for valuation in valuations:
                if valuation['quantity']>0:
                    cost = valuation['value']/valuation['quantity']
                    if cost>0:
                        rec.warehouse_cost_lines.create_update_costing(rec.product_variant_id,valuation['warehouse_id'],valuation['quantity'],cost)
                elif valuation['quantity']<=0:
                    costing = self.env['sh.warehouse.cost'].search(
                        [('product_id', '=', rec.product_variant_id.id), ('warehouse_id', '=', valuation['warehouse_id'][0])]).unlink()
                
            # rec.warehouse_cost_lines._compute_cost_warehouse_wise()
                
