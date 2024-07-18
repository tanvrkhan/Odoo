from odoo import models, fields
import requests
import logging
import datetime
from odoo.exceptions import UserError, Warning
from decimal import Decimal

_logger = logging.getLogger(__name__)

class TransferControllerBI(models.Model):
    _name = 'transfer.controller.bi'
    _description = 'Transfer Controller Business Intelligence'
    
    transfercontrollerbiid = fields.Integer(string="TransferControllerBiId")
    deliveryid = fields.Char(string="DeliveryId")
    fromtypeenum = fields.Char(string="FromTypeEnum")
    fromtypedisplayname = fields.Char(string="FromTypeDisplayName")
    frommotcode = fields.Char(string="FromMotCode")
    fromsubinventorycode = fields.Char(string="FromSubInventoryCode")
    totypeenum = fields.Char(string="ToTypeEnum")
    totypedisplayname = fields.Char(string="ToTypeDisplayName")
    tomotcode = fields.Char(string="ToMotCode")
    tosubinventorycode = fields.Char(string="ToSubInventoryCode")
    locationcode = fields.Char(string="LocationCode")
    deliveryprice = fields.Char(string="DeliveryPrice")
    deliverycommencementdate = fields.Char(string="DeliveryCommencementDate")
    deliverycompletiondate = fields.Char(string="DeliveryCompletionDate")
    deliveryatenum = fields.Char(string="DeliveryAtEnum")
    deliveryatdisplayname = fields.Char(string="DeliveryAtDisplayName")
    deliverystatusenum = fields.Char(string="DeliveryStatusEnum")
    finalizeddate = fields.Char(string="FinalizedDate")
    venturecode = fields.Char(string="VentureCode")
    hasattachmentdisplayname = fields.Char(string="HasAttachmentDisplayName")
    operatorpersoncode = fields.Char(string="OperatorPersonCode")
    blidcode = fields.Char(string="BlIdCode")
    bldate = fields.Char(string="BlDate")
    deliveryactivestatusenum = fields.Char(string="DeliveryActiveStatusEnum")
    deliveryactivestatusdisplayname = fields.Char(string="DeliveryActiveStatusDisplayName")
    mottypeenum = fields.Char(string="MotTypeEnum")
    mottypedisplayname = fields.Char(string="MotTypeDisplayName")
    deliverylocationcode = fields.Char(string="DeliveryLocationCode")
    inventoryid = fields.Char(string="InventoryId")
    deliverydate = fields.Char(string="DeliveryDate")
    fromstrategycode = fields.Char(string="FromStrategyCode")
    tostrategycode = fields.Char(string="ToStrategyCode")
    segmentid = fields.Char(string="SegmentId")
    fromgradecode = fields.Char(string="FromGradeCode")
    togradecode = fields.Char(string="ToGradeCode")
    titledeliverydate = fields.Char(string="TitleDeliveryDate")
    deliveryreference = fields.Char(string="DeliveryReference")
    trailerid = fields.Char(string="TrailerId")
    shapecode = fields.Char(string="ShapeCode")
    packagecount = fields.Char(string="PackageCount")
    consigneecounterpartcode = fields.Char(string="ConsigneeCounterpartCode")
    fromsegmentsectioncode = fields.Char(string="FromSegmentSectionCode")
    fromlocationcode = fields.Char(string="FromLocationCode")
    fromcounterpartcode = fields.Char(string="FromCounterpartCode")
    tosegmentsectioncode = fields.Char(string="ToSegmentSectionCode")
    tolocationcode = fields.Char(string="ToLocationCode")
    tocounterpartcode = fields.Char(string="ToCounterpartCode")
    concentratedisplayname = fields.Char(string="ConcentrateDisplayName")
    itineraryid = fields.Char(string="ItineraryId")
    fromtradestatusenum = fields.Char(string="FromTradeStatusEnum")
    totradestatusenum = fields.Char(string="ToTradeStatusEnum")
    tosegmentid = fields.Char(string="ToSegmentId")
    fromsegmentid = fields.Char(string="FromSegmentId")
    frommaterialcode = fields.Char(string="FromMaterialCode")
    tomaterialcode = fields.Char(string="ToMaterialCode")
    fromcommoditycode = fields.Char(string="FromCommodityCode")
    tocommoditycode = fields.Char(string="ToCommodityCode")
    fromassetcode = fields.Char(string="FromAssetCode")
    toassetcode = fields.Char(string="ToAssetCode")
    fromorigincode = fields.Char(string="FromOriginCode")
    toorigincode = fields.Char(string="ToOriginCode")
    frombrandcode = fields.Char(string="FromBrandCode")
    tobrandcode = fields.Char(string="ToBrandCode")
    fromshapecode = fields.Char(string="FromShapeCode")
    toshapecode = fields.Char(string="ToShapeCode")
    fromactualqty = fields.Char(string="FromActualQty")
    toactualqty = fields.Char(string="ToActualQty")
    fromactualqtyuomcode = fields.Char(string="FromActualQtyUomCode")
    toactualqtyuomcode = fields.Char(string="ToActualQtyUomCode")
    fromscheduledqty = fields.Char(string="FromScheduledQty")
    toscheduledqty = fields.Char(string="ToScheduledQty")
    fromscheduledqtyuomcode = fields.Char(string="FromScheduledQtyUomCode")
    toscheduledqtyuomcode = fields.Char(string="ToScheduledQtyUomCode")
    fromcontractqty = fields.Char(string="FromContractQty")
    fromcontractqtyuomcode = fields.Char(string="FromContractQtyUomCode")
    fromopenqty = fields.Char(string="FromOpenQty")
    toopenqty = fields.Char(string="ToOpenQty")
    fromopenqtyuomcode = fields.Char(string="FromOpenQtyUomCode")
    toopenqtyuomcode = fields.Char(string="ToOpenQtyUomCode")
    letterofcreditcode = fields.Char(string="LetterOfCreditCode")
    notifypartycode = fields.Char(string="NotifyPartyCode")
    totradenumber = fields.Char(string="ToTradeNumber")
    fromtradenumber = fields.Char(string="FromTradeNumber")
    fromphysicalmasterid = fields.Char(string="FromPhysicalMasterId")
    fromtradelocationcode = fields.Char(string="FromTradeLocationCode")
    fromtradeloadlocationcode = fields.Char(string="FromTradeLoadLocationCode")
    fromtradedischargelocationcode = fields.Char(string="FromTradeDischargeLocationCode")
    limitbreachdisplayname = fields.Char(string="LimitBreachDisplayName")
    fromscheduleplanningqty = fields.Char(string="FromSchedulePlanningQty")
    fromscheduleplanningqtyuomcode = fields.Char(string="FromSchedulePlanningQtyUomCode")
    fromactualplanningqty = fields.Char(string="FromActualPlanningQty")
    fromscheduleshippingqty = fields.Char(string="FromScheduleShippingQty")
    fromscheduleshippingqtyuomcode = fields.Char(string="FromScheduleShippingQtyUomCode")
    fromactualshippingqty = fields.Char(string="FromActualShippingQty")
    sapstatusdisplayname = fields.Char(string="SapStatusDisplayName")
    deliverytypeenum = fields.Char(string="DeliveryTypeEnum")
    deliverytypedisplayname = fields.Char(string="DeliveryTypeDisplayName")
    isintercompany = fields.Char(string="IsInterCompany")
    registrationnumber = fields.Char(string="RegistrationNumber")
    deliveryreference2 = fields.Char(string="DeliveryReference2")
    deliveryreference3 = fields.Char(string="DeliveryReference3")
    deliveryreference4 = fields.Char(string="DeliveryReference4")
    deliveryreference5 = fields.Char(string="DeliveryReference5")
    deliverytermcode = fields.Char(string="DeliveryTermCode")
    loadlocationcode = fields.Char(string="LoadLocationCode")
    dischargelocationcode = fields.Char(string="DischargeLocationCode")
    finaldestinationlocationcode = fields.Char(string="FinalDestinationLocationCode")
    drivername = fields.Char(string="DriverName")
    pricecurrencycode = fields.Char(string="PriceCurrencyCode")
    priceuomcode = fields.Char(string="PriceUomCode")
    billoflading = fields.Char(string="BillOfLading")
    lclpstart = fields.Char(string="LclpStart")
    lclpend = fields.Char(string="LclpEnd")
    lpnorberthing = fields.Char(string="LpNorBerthing")
    lpberthingdateetd = fields.Char(string="LpBerthingDateEtd")
    lparrival = fields.Char(string="LpArrival")
    lpdeparture = fields.Char(string="LpDeparture")
    dpnor = fields.Char(string="DpNor")
    dpberthing = fields.Char(string="DpBerthing")
    dparrival = fields.Char(string="DpArrival")
    dpdeparture = fields.Char(string="DpDeparture")
    frominternalcompany = fields.Char(string="FromInternalCompany")
    tointernalcompany = fields.Char(string="ToInternalCompany")
    indispute = fields.Char(string="InDispute")
    tsfromtypeenum = fields.Char(string="TsFromTypeEnum")
    tsfromtypedisplayname = fields.Char(string="TsFromTypeDisplayName")
    tstotypeenum = fields.Char(string="TsToTypeEnum")
    tstotypedisplayname = fields.Char(string="TsToTypeDisplayName")
    frominvoiceqty = fields.Char(string="FromInvoiceQty")
    frominvoiceqtyuom = fields.Char(string="FromInvoiceQtyUom")
    toinvoiceqtyuom = fields.Char(string="ToInvoiceQtyUom")
    toinvoiceqty = fields.Char(string="ToInvoiceQty")
    refdeliveryid = fields.Char(string="RefDeliveryId")
    storagetypeenum = fields.Char(string="StorageTypeEnum")
    storagetypedisplayname = fields.Char(string="StorageTypeDisplayName")
    incotermlocationcode = fields.Char(string="IncotermLocationCode")
    masterdealid = fields.Char(string="MasterDealId")
    referencenumber = fields.Char(string="ReferenceNumber")
    isfolioaccountnumber = fields.Char(string="IsFolioAccountNumber")
    folioaccountnumber = fields.Char(string="FolioAccountNumber")
    nominationkey = fields.Char(string="NominationKey")
    packagingclass = fields.Char(string="PackagingClass")
    packaginggroup = fields.Char(string="PackagingGroup")
    internalreference = fields.Char(string="InternalReference")
    internalreference1 = fields.Char(string="InternalReference1")
    inventorytypedisplayname = fields.Char(string="InventoryTypeDisplayName")
    businessunitcode = fields.Char(string="BusinessUnitCode")
    transportcarriagecode = fields.Char(string="TransportCarriageCode")
    tradeadmincode = fields.Char(string="TradeAdminCode")
    eventdatecolumn1 = fields.Char(string="EventDateColumn1")
    eventdatecolumn2 = fields.Char(string="EventDateColumn2")
    eventdatecolumn3 = fields.Char(string="EventDateColumn3")
    eventdatecolumn4 = fields.Char(string="EventDateColumn4")
    eventdatecolumn5 = fields.Char(string="EventDateColumn5")
    eventdatecolumn6 = fields.Char(string="EventDateColumn6")
    eventdatecolumn7 = fields.Char(string="EventDateColumn7")
    eventdatecolumn8 = fields.Char(string="EventDateColumn8")
    eventdatecolumn9 = fields.Char(string="EventDateColumn9")
    eventdatecolumn10 = fields.Char(string="EventDateColumn10")
    fromcropyearcode = fields.Char(string="FromCropYearCode")
    tocropyearcode = fields.Char(string="ToCropYearCode")
    fromvarietycode = fields.Char(string="FromVarietyCode")
    tovarietycode = fields.Char(string="ToVarietyCode")
    isfinalized = fields.Char(string="IsFinalized")
    vehiclecode = fields.Char(string="VehicleCode")
    priceentrytypeenum = fields.Char(string="PriceEntryTypeEnum")
    priceentrytypedisplayname = fields.Char(string="PriceEntryTypeDisplayName")
    vehiclemottypeenum = fields.Char(string="VehicleMotTypeEnum")
    vehiclemottypedisplayname = fields.Char(string="VehicleMotTypeDisplayName")
    commencementdate = fields.Char(string="CommencementDate")
    completiondate = fields.Char(string="CompletionDate")
    goodsreturndeletedate = fields.Char(string="GoodsReturnDeleteDate")
    goodsreturndescription = fields.Char(string="GoodsReturnDescription")
    carrier = fields.Char(string="Carrier")
    truckdriverid = fields.Char(string="TruckDriverId")
    stockholdno = fields.Char(string="StockHoldNo")
    customerno = fields.Char(string="CustomerNo")
    accountno = fields.Char(string="AccountNo")
    consignee = fields.Char(string="Consignee")
    trailer = fields.Char(string="Trailer")
    temperature = fields.Char(string="Temperature")
    gravitydensity = fields.Char(string="GravityDensity")
    issanction = fields.Char(string="IsSanction")
    description = fields.Char(string="Description")
    dealclassificationenum = fields.Char(string="DealClassificationEnum")
    dealclassificationdisplayname = fields.Char(string="DealClassificationDisplayName")
    productcode = fields.Char(string="ProductCode")
    carrierfein = fields.Char(string="CarrierFein")
    billtolocation = fields.Char(string="BillToLocation")
    transfercreationdate = fields.Char(string="TransferCreationDate")
    deliverygradecode = fields.Char(string="DeliveryGradeCode")
    weightfinalatdisplaytext = fields.Char(string="WeightFinalAtDisplayText")
    shiptolocationcode = fields.Char(string="ShipToLocationCode")
    fromcustomtradenumber = fields.Char(string="FromCustomTradeNumber")
    customsectionnumber = fields.Char(string="CustomSectionNumber")
    book = fields.Char(string="Book")
    frombookcode = fields.Char(string="FromBookCode")
    tobookcode = fields.Char(string="ToBookCode")
    nominationgroup = fields.Char(string="NominationGroup")
    lastvalueddate = fields.Char(string="LastValuedDate")
    isticketpresent = fields.Char(string="IsTicketPresent")
    operator = fields.Char(string="Operator")
    contracttypecode = fields.Char(string="ContractTypeCode")
    certificateno = fields.Char(string="CertificateNo")
    exchangecontractentrycode = fields.Char(string="ExchangeContractEntryCode")
    toexchangecontractentrycode = fields.Char(string="ToExchangeContractEntryCode")
    fromexchangecontractentrycode = fields.Char(string="FromExchangeContractEntryCode")
    istransferimported = fields.Char(string="IsTransferImported")
    buyselldisplaytext = fields.Char(string="BuySellDisplayText")
    portfoliocode = fields.Char(string="PortfolioCode")
    toistransit = fields.Char(string="ToIsTransit")
    periodtypeenumdisplaytext = fields.Char(string="PeriodTypeEnumDisplayText")
    fromistransit = fields.Char(string="FromIsTransit")
    toportfoliocode = fields.Char(string="ToPortfolioCode")
    frombuyselldisplaytext = fields.Char(string="FromBuySellDisplayText")
    tobuyselldisplaytext = fields.Char(string="ToBuySellDisplayText")
    deliverybasisofdisplaytext = fields.Char(string="DeliveryBasisOfDisplayText")
    agentname = fields.Char(string="AgentName")
    customtradenumber = fields.Char(string="CustomTradeNumber")
    gradecode = fields.Char(string="GradeCode")
    materialcode = fields.Char(string="MaterialCode")
    origincode = fields.Char(string="OriginCode")
    tradelinkid = fields.Char(string="TradeLinkId")
    statusenum = fields.Char(string="StatusEnum")
    modifypersonid = fields.Char(string="ModifyPersonId")
    lastmodifydate = fields.Char(string="LastModifyDate")
    modifyperson = fields.Char(string="ModifyPerson")
    customerid = fields.Char(string="CustomerId")
    lockid = fields.Char(string="LockId")
    birecordcreationdate = fields.Char(string="BiRecordCreationDate")
    def import_transfer(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/transfer"
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
                self.create_update_transfer('transfer', json_data)
                interface.update_sync_interface('transfer')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    def process_odoo_transaction_action(self):
        interface = self.env['fusion.sync.history']
        last_processing_date = interface.get_last_processing('transfer')
        trades_to_process = self.env['transfer.controller.bi'].search([('lastmodifydate', '>=', last_processing_date)])
        for rec in trades_to_process:
            rec.create_receipt()
        interface.update_processing_date('transfer')
    def sync_transfer(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('transfer')
        max_synced_date = self.env['transfer.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                        order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/transfer"
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
                self.create_update_transfer('transfer', json_data)
                interface.update_sync_interface('transfer')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_transfer(self, interface_type, json_data):
        if interface_type == 'transfer':
            all = self.env['transfer.controller.bi'].search([])
            if all:
                for data in json_data:
                    exists = all.search([('deliveryid', '=', data['deliveryid'])])
                    if exists:
                        return
                        # if exists:
                        #     return
                        # else:
                        #     self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
                        #     self.env['cashflow.controller.bi'].create(data)
                        #     self.env.cr.commit()
                    else:
                        self.env['transfer.controller.bi'].create(data)
                        self.env.cr.commit()
            else:
                for data in json_data:
                    self.env['transfer.controller.bi'].create(data)
                    self.env.cr.commit()
    
    def regular_update_transfer(self, interface_type, json_data):
        if interface_type == 'transfer':
            all = self.env['transfer.controller.bi'].search([])
            for data in json_data:
                exists = all.search([('deliveryid', '=', data['deliveryid'])])
                if exists:
                    self.env['transfer.controller.bi'].search([('deliveryid', '=', data['deliveryid'])]).unlink()
                    self.env['transfer.controller.bi'].create(data)
                else:
                    self.env['transfer.controller.bi'].create(data)
                    self.env.cr.commit()
    def get_quantity_from_controller(self,rec,product):
        if rec.fromcontractqtyuomcode == product.uom_id.name:
            return rec.fromactualqty if rec.fromactualqty else rec.fromscheduledqty
        elif rec.toactualqtyuomcode == product.uom_id.name:
            return rec.toactualqty if rec.toactualqty else rec.toscheduledqty
        elif rec.fromscheduledqty == rec.fromactualqty and rec.fromscheduledqtyuomcode == product.uom_id.name:
            return rec.fromactualqty
        # else:
        #     uom =''
        #     if rec.toactualqtyuomcode:
        #         quantity=rec.toactualqty
        #         uom = rec.toactualqtyuomcode
        #
        #     elif rec.fromactualqtyuomcode:
        #         quantity = rec.fromactualqty
        #         uom = rec.fromactualqtyuomcode
        #
        #     elif rec.fromscheduledqtyuomcode:
        #         quantity = rec.fromscheduledqty
        #         uom = rec.fromscheduledqtyuomcode
        #
        #     elif rec.toscheduledqtyuomcode:
        #         quantity = rec.toscheduledqty
        #         uom = rec.toscheduledqtyuomcode
        #
        #     conversion_rate = self.env['fusion.sync.history'].get_uom_conversion_factor(product, product.uom_id.name,uom)
        #     if conversion_rate:
        #         return quantity * conversion_rate
            
    def update_existing_lines(self,stock_move,product,rec,company,fromlocation,destlocation):
        lot = self.env['fusion.sync.history'].validate_lot(rec.itineraryid, product.id,
                                                           company.id)
        
        quantity = self.get_quantity_from_controller(rec,product)
        existing_line = stock_move.move_line_ids.filtered(
            lambda ml: ml.fusion_delivery_id == rec.deliveryid)
        if existing_line:
            for line in existing_line:
                if line.qty_done != float(quantity):
                    line.qty_done = quantity
                    line.location_id = fromlocation.id
                    line.location_dest_id = destlocation.id
        else:
            line = stock_move.move_line_ids.filtered(lambda ml: ml.product_id == product)
            if line:
                line.lot_id = lot.id
                i = 0
                for line2 in line:
                    if i == 0:
                        if line2.qty_done != float(quantity):
                            line2.qty_done = quantity
                            line2.fusion_delivery_id = rec.deliveryid
                            line2.location_id = fromlocation.id
                            line2.location_dest_id = destlocation.id
                            i += 1
            else:
                self.env['stock.move.line'].create({
                    'product_id': product.id,
                    'lot_id': lot.id,
                    'qty_done': quantity,
                    'move_id': stock_move.id,
                    'picking_id': stock_move.picking_id.id,
                    'location_id': fromlocation.id,
                    'location_dest_id': destlocation.id,
                    'fusion_delivery_id': rec.deliveryid,
                    'company_id': company.id
                })
                
    def fix_valuation_warehouse(self,picking,stock_move):
        for rec in self:
            if picking.location_id.usage == 'internal':
                stock_move.stock_valuation_layer_ids.warehouse_id = picking.location_id.warehouse_id.id
            elif picking.location_dest_id.usage == 'internal':
                stock_move.stock_valuation_layer_ids.warehouse_id = picking.location_dest_id.warehouse_id.id
    def create_receipt(self):
        for record in self:
            # try:
                random_string = self.env['fusion.sync.history'].generate_random_string()
                all_transfers = self.env['transfer.controller.bi'].search([('itineraryid', '=', record.itineraryid)])
                sms = self.env['stock.move'].search([])
                pickings = self.env['stock.picking'].search([])
                for rec in all_transfers:
                    
                    
                    if (rec.frominternalcompany if rec.frominternalcompany else rec.tointernalcompany) == self.env.company.name:
                        if rec.deliveryactivestatusdisplayname=="Active":
                            company = self.env['res.company'].search([('name', '=', rec.frominternalcompany)], limit=1)
                            if not company:
                                company = self.env['res.company'].search([('name', '=', rec.tointernalcompany)],
                                                                         limit=1)
                            if rec.deliverystatusenum in ('Actual','Scheduled'):
                                pol = self.env['purchase.order.line'].search([('fusion_segment_code', '=', rec.fromsegmentsectioncode if rec.fromsegmentsectioncode else '100')], limit=1)
                                po = self.env['purchase.order'].search([('id', '=', pol.order_id.id)])
                                sol = self.env['sale.order.line'].search(
                                    [('fusion_segment_code', '=', rec.tosegmentsectioncode  if rec.tosegmentsectioncode else '100')], limit=1)
                                so = self.env['sale.order'].search([('id', '=', sol.order_id.id)])
                                cf = self.env['cashflow.controller.bi'].search([('transfernumber', '=', rec.deliveryid),('costtype', '=', 'Primary Settlement')],limit=1)
                                exists = self.env['stock.move'].search([('id', '=', '0')])
                                stock_move = self.env['stock.move'].search([('id', '=', '0')])
            
                                product = self.env['product.product'].search([('id', '=', '0')], limit=1)
                                nomination_link = self.env['fusion.sync.history'].checkAndDefineAnalytic('Nomination',
                                                                                                         rec.itineraryid,
                                                                                                         company.id)
                                warehouse = self.env['stock.warehouse'].search([('id', '=', '0')], limit=1)
                                existing_distribution=[]
                                
                                if rec.totypeenum == 'Trade' or rec.fromtypeenum == 'Trade':
                                    exists = sms.search(
                                        [('fusion_delivery_id', '=', rec.deliveryid)], limit=1)
                                    if exists:
                                        if exists.fusion_last_modify == self.parse_datetime(rec.lastmodifydate) and exists.state=='done':
                                            continue
                                        else:
                                            exists.fusion_delivery_id = rec.deliveryid
                                            exists.fusion_last_modify = self.parse_datetime(rec.lastmodifydate)
                                            exists = sms.search([('id', '=', exists.id)])
                                            picking = exists.picking_id
                                            if picking.state  in ('done','waiting','confirmed','cancel'):
                                                picking.set_stock_move_to_draft()
                                                picking.action_confirm()
                                            self.update_existing_lines(exists, exists.product_id, rec, company,picking.location_id,picking.location_dest_id)
                                            self.confirm_picking(picking)
                                            continue
                                            
                                    else:
                                        if rec.buyselldisplaytext=="Buy":
                                            if po:
                                                if pol:
                                                    if not po.state == 'purchase':
                                                        po.button_confirm()
                                                        # self.env.cr.commit()
                                                    product = pol.product_id
                                                    storage_link = self.env['fusion.sync.history'].checkAndDefineAnalytic('Deal Reference',
                                                                                                                          rec.tomotcode,
                                                                                                                          company.id)
                                                  
                                                    
                                                    
                                                    warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.tomotcode,
                                                                                                                   company)
                                                    
                                                    existing_distribution = pol.analytic_distribution
                                                    existing_distribution[str(nomination_link.id)] = 100
                                                    existing_distribution[str(storage_link.id)] = 100
                                                    pol['analytic_distribution'] = existing_distribution
                                                    exists = sms.search(
                                                        [('fusion_delivery_id', '=', rec.deliveryid), ('purchase_line_id', '=', pol.id)],
                                                        limit=1)
                                                    if exists:
                                                        stock_move = sms.search([('id', '=', exists.id)])
                                                    else:
                                                        stock_move = sms.search(
                                                            [('purchase_line_id', '=', pol.id), ('state', 'in', ('assigned','waiting','confirmed','draft'))], limit=1)
                                                        if not stock_move:
                                                            stock_move_posted = sms.search(
                                                                [('purchase_line_id', '=', pol.id), ('state', '=', 'done')], limit=1)
                                                            if stock_move_posted:
                                                                stock_move = stock_move_posted.copy()
                                                        if not stock_move:
                                                            res = pol.order_id._prepare_picking()
                                                            picking = self.env['stock.picking'].create(res)
                                                            stock_move = pol._create_stock_moves(picking[0])
                                                            
                                                
                                                    
                                        elif rec.tobuyselldisplaytext=="Sell":
                                            if so:
                                                if sol:
                                                    warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.frommotcode,
                                                                                                                   company)
                                                    so.warehouse_id = warehouse
                                                    if not so.state == 'sale':
                                                        so.action_confirm()
                                                        # self.env.cr.commit()
                                                    product = sol.product_id
                                                    storage_link = self.env['fusion.sync.history'].checkAndDefineAnalytic('Deal Reference',
                                                                                                                          rec.frommotcode,
                                                                                                                          company.id)
                                                    existing_distribution = sol.analytic_distribution
                                                    existing_distribution[str(nomination_link.id)] = 100
                                                    existing_distribution[str(storage_link.id)] = 100
                                                    sol['analytic_distribution'] = existing_distribution
                                                    picking_type = self.env['stock.picking.type'].search(
                                                        [('code', '=', 'outgoing'),
                                                         ('warehouse_id', '=', warehouse.id)], limit=1)
                                                    out_location = self.env['stock.location'].search(
                                                        [('warehouse_id', '=', warehouse.id)], limit=1)
                                                    exists = sms.search(
                                                        [('fusion_delivery_id', '=', rec.deliveryid), ('sale_line_id', '=', sol.id)],
                                                        limit=1)
                                                    if exists:
                                                        stock_move = sms.search([('id', '=', exists.id)])
                                                    else:
                                                        stock_move = sms.search(
                                                            [('sale_line_id', '=', sol.id), ('state', 'in', ('assigned', 'waiting', 'confirmed', 'draft'))], limit=1)
                                                        if not stock_move:
                                                            stock_move_posted = sms.search(
                                                                [('sale_line_id', '=', sol.id), ('state', '=', 'done')], limit=1)
                                                            if stock_move_posted:
                                                                stock_move = stock_move_posted.copy()
                                                        if not stock_move:
                                                            picking = {
                                                                'partner_id': so.partner_id.id,
                                                                'picking_type_id': picking_type.id,
                                                                'location_id': out_location.id,
                                                                'move_type': 'direct',
                                                                'company_id': company.id,
                                                                'sale_id': so.id,
                                                                'origin': so.name
                                                            }
                                                            
                                                            picking = self.env['stock.picking'].create(picking)
                                                            move_vals = {
                                                                'name': product.name,
                                                                'product_id': product.id,
                                                                'fusion_delivery_id': rec.deliveryid,
                                                                'product_uom': product.uom_id.id,
                                                                'picking_id': picking.id,
                                                                'location_id': out_location.id,
                                                                'location_dest_id': picking.location_dest_id.id,
                                                                'sale_line_id': sol.id
                                                            }
                                                            stock_move = sms.create(move_vals)
                                                            picking.sale_id=so.id
                                    if po or so:
                                        if stock_move and (stock_move.fusion_last_modify != self.parse_datetime(rec.lastmodifydate) or stock_move.state!='done'):
                                            picking = stock_move.picking_id
                                            stock_move.fusion_last_modify = self.parse_datetime(rec.lastmodifydate)
                                            if product.uom_id.rounding != 0.001:
                                                product.uom_id.rounding = 0.001
                                            picking.fusion_segment_code = pol.fusion_segment_code
                                            picking.fusion_itinerary_id = rec.itineraryid
                                            stock_move.fusion_delivery_id = rec.deliveryid
                                            stock_move.fusion_segment_code = pol.fusion_segment_code
                                            if rec.deliverycompletiondate or rec.bldate or rec.titledeliverydate:
                                                if stock_move.state in('done','waiting','confirmed','assigned'):
                                                    stock_move.picking_id.set_stock_move_to_draft()
                                                # stock_move.picking_id.deal_ref = 'moved_to_Draft'
                                                picking.custom_delivery_date = self.parse_datetime(
                                                    rec.deliverycompletiondate if rec.deliverycompletiondate else rec.bldate if rec.bldate else rec.titledeliverydate)
                                                picking.date_done = self.parse_datetime(
                                                    rec.deliverycompletiondate if rec.deliverycompletiondate else rec.bldate if rec.bldate else rec.titledeliverydate)
                                                picking.scheduled_date = self.parse_datetime(
                                                    rec.deliverycompletiondate if rec.deliverycompletiondate else rec.bldate if rec.bldate else rec.titledeliverydate)
                                                stock_move.date = self.parse_datetime(rec.deliverycompletiondate  if rec.deliverycompletiondate else rec.bldate if rec.bldate else rec.titledeliverydate)
                                                
                                                if rec.buyselldisplaytext == "Buy":
                                                    picking_type = self.env['stock.picking.type'].search(
                                                        [('code', '=', 'incoming'), ('warehouse_id', '=', warehouse.id)], limit=1)
                                                if not picking_type:
                                                    picking_type=picking.picking_type_id
                                                picking.picking_type_id = picking_type
                                                stock_move.location_id = picking.location_id,
                                                stock_move.location_dest_id = picking.location_dest_id,
                                                self.update_existing_lines(stock_move,product,rec,company,picking.location_id,picking.location_dest_id)
                                                self.confirm_picking(picking)
                                                if rec.buyselldisplaytext == "Sell":
                                                    picking.sale_id=so.id
                                            
                                                    
                                            # self.fix_valuation_warehouse(picking,stock_move)
                                            # self.env.cr.commit()
                                            # stock_move.stock_valuation_layer_ids.recalculate_stock_value()
                                    else:
                                        if rec.frombuyselldisplaytext == "Buy":
                                            log_error = self.env['fusion.sync.history.errors'].log_error('TransferController',
                                                                                                         rec.fromsegmentid,
                                                                                                         'PO Line not found',
                                                                                                         rec.frominternalcompany)
                                        else:
                                            log_error = self.env['fusion.sync.history.errors'].log_error('TransferController',
                                                                                                     rec.tosegmentid,
                                                                                                     'SO Line not found',
                                                                                                     rec.tointernalcompany)
                                        raise UserError("Order not found." + rec.tosegmentsectioncode if rec.tosegmentsectioncode else rec.fromsegmentsectioncode + rec.buyselldisplaytext)
                                elif rec.fromcommoditycode!='Coal' and rec.tocommoditycode!='Coal' and (rec.fromtypeenum!='Trade' and rec.totypeenum!='Trade'):
                                    companies = []
                                    all_companies = self.env['res.company'].search([])
                                    for company in all_companies:
                                        companies.append(company.name)
                                    company = self.env['res.company'].search([('name', '=', rec.frominternalcompany)],
                                                                             limit=1)
                                    if not company:
                                        company = self.env['res.company'].search([('name', '=', rec.tointernalcompany)],
                                                                                 limit=1)
                                        if not company:
                                            pt = self.env['transfer.controller.bi'].search([('itineraryid', '=', rec.itineraryid),('tointernalcompany', 'in', (companies))],
                                                                                 limit=1)
                                            if not pt:
                                                pt = self.env['transfer.controller.bi'].search(
                                                    [('itineraryid', '=', rec.itineraryid),
                                                     ('frominternalcompany', '!=', False)],
                                                    limit=1)
                                            company = self.env['res.company'].search([('name', '=', pt.tointernalcompany if pt.tointernalcompany else pt.frominternalcompany)],
                                                                             limit=1)
                                    product = self.env['fusion.sync.history'].validate_product(rec.fromcommoditycode,
                                                                                               rec.frommaterialcode,
                                                                                               rec.fromactualqtyuomcode)
                                    lot = self.env['fusion.sync.history'].validate_lot(rec.itineraryid, product.id,
                                                                                       company.id)
                                  
                                    in_warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.frommotcode,
                                                                                                   company)
                                    in_location = self.env['stock.location'].search(
                                        [('warehouse_id', '=', in_warehouse.id)], limit=1)
                                    picking_type = self.env['stock.picking.type'].search(
                                        [('code', '=', 'internal'), ('warehouse_id', '=', in_warehouse.id)], limit=1)
                                    
                                    out_warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.tomotcode,
                                                                                                      company)
                                    out_location = self.env['stock.location'].search(
                                        [('warehouse_id', '=', out_warehouse.id)], limit=1)
                                    
                                    
                                    stock_move = sms.search([('id', '=', 0)])
                                    
                                    exists = sms.search(
                                        [('fusion_delivery_id', '=', rec.deliveryid)],
                                        limit=1)
                                    if not exists:
                                        if product.uom_id.rounding != 0.001:
                                            product.uom_id.rounding = 0.001
                                        picking_vals = {
                                            'picking_type_id': picking_type.id,
                                            'location_id': in_location.id,
                                            'location_dest_id': out_location.id,
                                            'move_type': 'direct',
                                            'fusion_delivery_id': rec.deliveryid,
                                        }
                                        picking = self.env['stock.picking'].create(picking_vals)
                                        quantity = self.get_quantity_from_controller(rec,product)
                                        
                                        move_vals = {
                                            'name': 'Internal Transfer ' + str(rec.frommotcode) + ' - ' + str(
                                                rec.tomotcode),
                                            'product_id': product.id,
                                            'product_uom_qty': quantity,
                                            'fusion_delivery_id': rec.deliveryid,  #
                                            'product_uom': product.uom_id.id,
                                            'picking_id': picking.id,
                                            'location_id': in_location.id,
                                            'location_dest_id': out_location.id,
                                        }
                                        stock_move = sms.create(move_vals)
                                        stock_move.move_line_ids.lot_id=lot
                                        stock_move.move_line_ids.fusion_delivery_id = rec.deliveryid,  #
                                        picking.action_confirm()
                                        picking.action_assign()
                                        self.confirm_picking(picking)

                                        
                        else:
                            cancelled_entry = self.env['stock.move'].search(
                                [('fusion_delivery_id', '=', rec.deliveryid)])
                            if cancelled_entry:
                                cancelled_entry.picking_id.set_stock_move_to_draft()
                self.env.cr.commit()
            # except Exception as e:
            #     log_error = self.env['fusion.sync.history.errors'].log_error('TransferController', rec.fromsegmentid,
            #                                                                  str(e),
            #                                                                  rec.tointernalcompany)
            #     raise UserError( str(e) + str(rec))
                
        
                # _logger.error('Error processing API data: %s', str(e))
                # if pol:
                #     pol = self.env['purchase.order.line'].search([('fusion_segment_id', '=', pol.termnumber)],limit=1)
                #     po = self.env['purchase.order'].search([('id', '=', pol.order_id.id)])
                #       stock_moves = self.env['stock.move'].search([('purchase_line_id', '=', pol.id)])
                #     picking_ids = set()
                #     for move in stock_moves:
                #         if move.picking_id:
                #             picking_ids.add(move.picking_id.id)
                #             if len(picking_ids):
                #                 a=True
                #
        
    def confirm_picking(self,picking):
        a=1
        picking.button_validate()
        if picking.state!='done':
            picking._action_done()
        self.env.cr.commit()
    
    def parse_datetime(self,time_str):
        try:
            # First try parsing with fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            # If it fails, try parsing without fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
                