# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import formatLang


class InheritSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_cost = fields.Many2one("purchase.order.line", "Product Cost")

    @api.onchange('product_id')
    def get_rel_purchases_line(self):
        for rec in self:
            domain = {
                'domain': {
                    'product_cost': [('product_id', '=', rec.product_id.id), ('order_id.state', '=', 'purchase')]}}
            return domain


class InheritPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        if self.env.context.get('check_cost'):
            lines = self.env['purchase.order.line'].search([('product_id.id', '=', self.env.context.get('product_id'))])
            for rec in lines:
                name = '%s %s' % (rec.order_id.name, rec.price_unit)
                result.append((rec.id, name))
            return result
        else:
            for rec in self:
                name = '%s' % rec.price_unit
                result.append((rec.id, name))
        return result
