# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from odoo.tools import float_is_zero, float_repr


class ProductTmpl(models.Model):
    _inherit = "product.product"

    warehouse_cost_lines = fields.One2many('sh.warehouse.cost', 'product_id')

    def _stock_account_get_anglo_saxon_price_unit(self, uom=False, warehouse=False):
        # * Softhealer code Start *

        # Added warehouse in the argument and setting price based on warehouse

        # * Softhealer code end *

        price = 0.0
        if warehouse:
            price = self.warehouse_cost_lines.filtered(
                lambda x: x.warehouse_id.id == warehouse).cost
        else:
            price = self.standard_price
        if not self or not uom or self.uom_id.id == uom.id:
            return price or 0.0
        return self.uom_id._compute_price(price, uom)

    def _prepare_out_svl_vals(self, quantity, company, warehouse=False):
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
            'quantity': quantity
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
