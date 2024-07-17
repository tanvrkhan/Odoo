from odoo import models, fields, api
import requests
import logging
import datetime
from odoo.exceptions import UserError, Warning
_logger = logging.getLogger(__name__)

from odoo import models, fields

class StorageInspectorBuildDrawDataBI(models.Model):
    _name = 'stockadjustments.controller.bi'
    _description = 'Storage Inspector Build Draw Data BI'

    motid = fields.Integer(string='Mot ID')
    subinventoryid = fields.Integer(string='Sub Inventory ID')
    storagetype = fields.Char(string='Storage Type')
    storage = fields.Char(string='Storage')
    level = fields.Char(string='Level')
    builddraw = fields.Char(string='Build Draw')
    tradenumber = fields.Integer(string='Trade Number')
    transfernumber = fields.Integer(string='Transfer Number')
    effectivedate = fields.Date(string='Effective Date')
    material = fields.Char(string='Material')
    builddrawtype = fields.Char(string='Build Draw Type')
    builddrawqty = fields.Float(string='Build Draw Qty')
    operator = fields.Char(string='Operator')
    editedby = fields.Char(string='Edited By')
    openqty = fields.Float(string='Open Qty')
    netqty = fields.Float(string='Net Qty')
    transfercommencementdate = fields.Date(string='Transfer Commencement Date')
    transfercompletiondate = fields.Date(string='Transfer Completion Date')
    status = fields.Char(string='Status')
    deliveryactivestatusenum = fields.Char(string='Delivery Active Status Enum')
    goodsreturnsystemdate = fields.Date(string='Goods Return System Date')
    goodsreturndate = fields.Date(string='Goods Return Date')
    goodsreturndescription = fields.Text(string='Goods Return Description')
    builddrawnum = fields.Integer(string='Build Draw Num')
    person = fields.Char(string='Person')
    editedon = fields.Date(string='Edited On')
    buysection = fields.Char(string='Buy Section')
    voyagesegment = fields.Char(string='Voyage Segment')
    deliverydate = fields.Date(string='Delivery Date')
    deliverystatus = fields.Char(string='Delivery Status')
    registrationno = fields.Char(string='Registration No')
    applicationdate = fields.Date(string='Application Date')
    bldate = fields.Date(string='BL Date')
    blnumber = fields.Char(string='BL Number')
    segmentreference = fields.Text(string='Segment Reference')
    weightedaverage = fields.Float(string='Weighted Average')
    transferat = fields.Char(string='Transfer At')
    transferprice = fields.Float(string='Transfer Price')
    deliverytypeenum = fields.Char(string='Delivery Type Enum')
    mtmprice = fields.Float(string='MTM Price')
    mtmpnl = fields.Float(string='MTM PnL')
    folioaccount = fields.Char(string='Folio Account')
    imported = fields.Char(string='Imported')
    folioaccountnumber = fields.Char(string='Folio Account Number')
    ventureid = fields.Char(string='Venture ID')
    deliveryticketid = fields.Integer(string='Delivery Ticket ID')
    ticketnumber = fields.Integer(string='Ticket Number')
    transporter = fields.Char(string='Transporter')
    drivername = fields.Char(string='Driver Name')
    driverid = fields.Char(string='Driver ID')
    ticketreference1 = fields.Char(string='Ticket Reference 1')
    ticketreference2 = fields.Char(string='Ticket Reference 2')
    ticketreference3 = fields.Char(string='Ticket Reference 3')
    pedimentonumber = fields.Text(string='Pedimento Number')
    externalref1 = fields.Char(string='External Ref 1')
    externalref2 = fields.Char(string='External Ref 2')
    statusenum = fields.Boolean(string='Status Enum')
    modifypersonid = fields.Integer(string='Modify Person ID')
    lastmodifydate = fields.Char(string='Last Modify Date')
    modifyperson = fields.Char(string='Modify Person')
    customerid = fields.Integer(string='Customer ID')
    lockid = fields.Integer(string='Lock ID')
    birecordcreationdate = fields.Date(string='BI Record Creation Date')
    internalcompany = fields.Char(string='Internal Company')
    counterparty = fields.Char(string='Counterparty')
    quantityuom = fields.Char(string='Quantity UOM')

    def import_stock_adjustments(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/StockAdjustments"
        headers = {
            'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
            'Content-Type': 'application/json',
        }
        params = {
            'date': last_sync
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                json_data = response.json()
                json_data = interface.lowercase_keys(json_data)
                # for data in json_data:
                self.create_update_stock_adjustments('StockAdjustments', json_data)
                interface.update_sync_interface('StockAdjustments')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_stock_adjustments(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('stockadjustments')
        max_synced_date = self.env['stockadjustments.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                         order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/StockAdjustments"
        headers = {
            'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
            'Content-Type': 'application/json',
        }
        params = {
            'date': last_sync
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                json_data = response.json()
                json_data = interface.lowercase_keys(json_data)
                # for data in json_data:
                self.create_update_stock_adjustments('stockadjustments', json_data)
                interface.update_sync_interface('stockadjustments')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
            
   
    def create_update_stock_adjustments(self, interface_type, json_data):
        all = self.env['stockadjustments.controller.bi'].search([])
        if all:
            for data in json_data:
                exists = all.search([('builddrawnum', '=', data['builddrawnum'])])
                if exists:
                    if exists.lastmodifydate == data['lastmodifydate']:
                        continue
                    else:
                        all.search([('builddrawnum', '=', data['builddrawnum'])]).unlink()
                        self.env['stockadjustments.controller.bi'].create(data)
                        self.env.cr.commit()
                else:
                    self.env['stockadjustments.controller.bi'].create(data)
                    self.env.cr.commit()
        else:
             for data in json_data:
                 self.env['stockadjustments.controller.bi'].create(data)
                 self.env.cr.commit()
    
    def regular_update_stock_adjustments(self, interface_type, json_data):
        all = self.env['stockadjustments.controller.bi'].search([])
        for data in json_data:
            exists = all.search([('editedon', '=', data['editedon'])])
            if exists:
                continue
            else:
                self.env['stockadjustments.controller.bi'].create(data)
    def create_transfer(self):
        for rec in self:
            if rec.status=='Active':
                if rec.internalcompany:
                    company = self.env['res.company'].search([('name', '=', rec.internalcompany)], limit=1)
                    if company:
                        balancing_warehouse =  self.env['fusion.sync.history'].validate_warehouse('Stock Adjustments',company)
                        warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.storage,company)
                        if balancing_warehouse and warehouse:
                            rec.create_picking(rec,balancing_warehouse,warehouse,company)
                else:
                    raise UserError("Company is not selected on storage level in Fusion.")
            else:
                exists = self.env['stock.picking'].search([('fusion_build_draw', '=', rec.builddrawnum)])
                if exists:
                    exists.set_stock_move_to_draft()
                    exists.action_cancel()
                    

    
    def create_picking(self,rec,balancing_warehouse,warehouse,company):
        existing_picking = self.env['stock.picking'].search([('fusion_build_draw', '=', self.builddrawnum)])
        if existing_picking:
            if existing_picking.move_ids.fusion_last_modify == self.parse_datetime(rec.lastmodifydate):
                return
            else:
                existing_picking.set_stock_move_to_draft()
                existing_picking.action_confirm()
                existing_picking.valuation_price= rec.transferprice
                existing_picking.move_ids.line_ids.qty_done = rec.quantity
                existing_picking.button_validate()
        else:
            picking_type = self.env['stock.picking.type'].search(
                [('sequence_code', '=', 'INT'), ('warehouse_id', '=', warehouse.id)], limit=1)
            warehouse_location = self.env['stock.location'].search([('warehouse_id', '=', warehouse.id),('name','=','Stock')], limit=1)
            balancing_warehouse_location = self.env['stock.location'].search([('warehouse_id', '=', balancing_warehouse.id),('name','=','Stock')], limit=1)
            product_templ = self.env['product.template'].search([('name', '=', rec.material),('default_code', '=', 'I')],
                                                              limit=1)
            product= self.env['product.product'].search([('product_tmpl_id', '=', product_templ.id)], limit=1)
            
            uom = self.env['fusion.sync.history'].validate_uom(product,
                                                               rec.quantityuom)
            lot = self.env['fusion.sync.history'].validate_lot(rec.transfernumber, product.id,
                                                               company.id)
            
            in_location = self.env['stock.location']
            out_location = self.env['stock.location']
            if uom.rounding != 0.001:
                uom.rounding = 0.001
            if rec.builddrawqty>0:
                in_location = warehouse_location
                out_location = balancing_warehouse_location
            else:
                in_location = balancing_warehouse_location
                out_location = warehouse_location
            
            if product.uom_id.rounding != 0.001:
                product.uom_id.rounding = 0.001
            picking_vals = {
                'picking_type_id': picking_type.id,
                'location_id': out_location.id,
                'location_dest_id': in_location.id,
                'move_type': 'direct',
                'valuation_price': rec.transferprice,
                'company_id': company.id,
                'fusion_build_draw': rec.builddrawnum
            }
            picking = self.env['stock.picking'].create(picking_vals)
            quantity = rec.builddrawqty if rec.builddrawqty > 0 else rec.builddrawqty *-1
            
            move_vals = {
                'name': 'Internal Transfer ' + str(rec.storage),
                'product_id': product.id,
                'product_uom_qty': quantity,
                'product_uom': uom.id,
                'picking_id': picking.id,
                'location_id': out_location.id,
                'location_dest_id': in_location.id,
                'quantity_done': quantity,
                'company_id': company.id, #
            }
            stock_move = self.env['stock.move'].create(move_vals)
            stock_move.move_line_ids.lot_id = lot
            stock_move.fusion_last_modify = self.parse_datetime(rec.lastmodifydate)
            picking.action_confirm()
            picking.action_assign()
            self.confirm_picking(picking)
        
    def parse_datetime(self,time_str):
        try:
            # First try parsing with fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            # If it fails, try parsing without fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
    def confirm_picking(self,picking):
        a=1
        picking.button_validate()
        if picking.state!='done':
            picking._action_done()
        self.env.cr.commit()