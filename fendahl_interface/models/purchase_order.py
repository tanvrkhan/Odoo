import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime
from odoo.exceptions import ValidationError


class PurchaseOrderSync(models.Model):
    _inherit = 'purchase.order'
    fusion_deal_number = fields.Char('Deal')
    
    def cancel(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([('purchase_id', '=', rec.id)])
            for picking in pickings:
                picking.set_stock_move_to_draft()
            invoices = self.invoice_ids
            for invoice in invoices:
                invoice.button_draft()
                invoice.button_draft()
            rec.button_draft()
            rec.button_cancel()

class PurchaseOrderLineSync(models.Model):
    _inherit = 'purchase.order.line'
    
    fusion_segment_id = fields.Integer('Fusion Section Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    custom_section_number = fields.Char('Fusion Custom Section Number')


class SaleOrderSync(models.Model):
    _inherit = 'sale.order'
    fusion_deal_number = fields.Char('Deal')
    

class SaleOrderLineSync(models.Model):
    _inherit = 'sale.order.line'
    
    fusion_segment_id = fields.Integer('Fusion Section Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    custom_section_number = fields.Char('Fusion Custom Section Number')


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')
    fusion_segment_code = fields.Char('Fusion Section Code')

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    update_identity = fields.Boolean('Update Identity')
    fusion_last_modify = fields.Datetime(string="Fusion Last Modify")
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    fusion_delivery_id = fields.Char('Fusion Delivery ID')

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    custom_section_no = fields.Char('Depricated')
    fusion_segment_code = fields.Char('Fusion Section Code')
    custom_section_number = fields.Char('Fusion Custom Section Number')
    


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    custom_section_no = fields.Char('Depricated')
    custom_section_number = fields.Char('Fusion Custom Section Number')
    fusion_segment_code = fields.Char('Fusion Section Code')
    cashflow_id = fields.Integer('Cashflow Id')