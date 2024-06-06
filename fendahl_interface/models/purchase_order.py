import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, Warning

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
    
    def fetch_from_controller(self):
        for rec in self:
            if rec.fusion_segment_code:
                self.env['trade.controller.bi'].search([('segmentsectioncode', '=', rec.fusion_segment_code)]).create_order()
            else:
                raise UserError("Order isn't from Fusion.")


class SaleOrderSync(models.Model):
    _inherit = 'sale.order'
    fusion_deal_number = fields.Char('Deal')

class SaleOrderLineSync(models.Model):
    _inherit = 'sale.order.line'
    
    fusion_segment_id = fields.Integer('Fusion Section Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    custom_section_number = fields.Char('Fusion Custom Section Number')
    
    def fetch_from_controller(self):
        for rec in self:
            if rec.fusion_segment_code:
                self.env['trade.controller.bi'].search([('segmentsectioncode', '=', rec.fusion_segment_code)]).create_order()
            else:
                raise UserError("Order isn't from Fusion.")


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    fusion_itinerary_id = fields.Char('Nomination No.')

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    fusion_delivery_id = fields.Integer('Fusion Delivery Id')
    fusion_segment_code = fields.Char('Fusion Section Code')
    update_identity = fields.Boolean('Update Identity')
    fusion_last_modify = fields.Datetime(string="Fusion Last Modify")
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    fusion_delivery_id = fields.Char('Fusion Delivery ID')
    
    def force_delete(self):
        for rec in self:
            if not rec.move_id.picking_id:
                rec.state='draft'
                rec.move_id.state='draft'
                ml = rec.id
                m = rec.move_id.id
                self.env['stock.move.line'].search([('id','=',ml)]).unlink()
                self.env['stock.move'].search([('id', '=', m)]).unlink()

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
    
    def fetch_invoice_from_controller(self):
        for rec in self:
            if rec.move_id.fusion_reference:
                invoicenumber = rec.move_id.fusion_reference.split(',')[0]
                if invoicenumber:
                    controllerinvoice = self.env['invoice.controller.bi'].search([('invoicenumber','=',invoicenumber)],limit=1)
                    if controllerinvoice:
                        controllerinvoice.create_bill(True)
                    else:
                        raise UserError('The invoice doesnt exist in fusion controller')
            else:
                raise UserError('The invoice is not from Fusion')
