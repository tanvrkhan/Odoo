# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class WarehouseCosting(models.Model):
    _name = "sh.warehouse.cost"
    _description = "Stores Cost warehouse Wise"

    product_id = fields.Many2one('product.product', string="Product")
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    cost = fields.Float("Cost")
    sh_onhand_qty = fields.Float("Onhand Quantity",compute="_compute_onhand_warehouse_wise")

    def _compute_onhand_warehouse_wise(self):
        for rec in self:
            rec.sh_onhand_qty=0.0
            if rec.warehouse_id:
                quantity=sum(self.env['stock.quant'].search([('product_id','=',rec.product_id.id)]).filtered(lambda x:x.location_id.warehouse_id.id == rec.warehouse_id.id).mapped('quantity'))
                rec.sh_onhand_qty=quantity
                
    # def _compute_cost_warehouse_wise(self):
    #     for rec in self:
    #         rec.cost = 0
    #         valuations = self.env['stock.valuation.layer'].search([('product_id','=',rec.product_id.id),('company_id','=',self.env.company.id),('warehouse_id','=',rec.warehouse_id.id)])
    #         if valuations:
    #             amount = sum(valuations.mapped(lambda r: r.value))
    #             quantity = sum(valuations.mapped(lambda r: r.quantity))
    #             if amount > 0 and quantity > 0:
    #                 cost = amount / quantity
    #                 rec.cost=cost
    #             else:
    #                 rec.cost =0
    def create_update_costing(self,product_id,warehouse_id, quantity, value):
        costing = self.env['sh.warehouse.cost'].search([('product_id','=',product_id.id),('warehouse_id','=',warehouse_id[0])])
        if costing:
            costing.sh_onhand_qty =quantity
            costing.cost = value
        else:
            self.env['sh.warehouse.cost'].create({
                'warehouse_id':warehouse_id[0],
                'product_id':product_id.id,
                'sh_onhand_qty':round(quantity,3),
                'cost':round(value,2)
            })
    
        