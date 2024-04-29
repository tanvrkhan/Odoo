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
            rec.button_draft()
            rec.button_cancel()

class PurchaseOrderLineSync(models.Model):
    _inherit = 'purchase.order.line'
    
    fusion_segment_id = fields.Integer('Fusion Section Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    custom_section_number = fields.Char('Fusion Custom Section Number')
    


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    custom_section_no = fields.Char('Depricated')
    custom_section_number = fields.Char('Fusion Custom Section Number')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    custom_section_no = fields.Char('Depricated')
    custom_section_number = fields.Char('Fusion Custom Section Number')