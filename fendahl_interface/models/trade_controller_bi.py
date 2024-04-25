from odoo import models, fields
import requests
import logging
import datetime
from odoo.exceptions import UserError, Warning
from decimal import Decimal
_logger = logging.getLogger(__name__)

class TradeControllerBI(models.Model):
    _name = 'trade.controller.bi'
    _description = 'Trade Controller BI'
    
    dealmasterid = fields.Char(string="DealMasterId")
    segmentid = fields.Char(string="SegmentId")
    externalref = fields.Char(string="ExternalRef")
    tradedate = fields.Char(string="TradeDate")
    internalcompany = fields.Char(string="InternalCompany")
    counterpartcompany = fields.Char(string="CounterpartCompany")
    traderperson = fields.Char(string="TraderPerson")
    segmentsectioncode = fields.Char(string="SegmentSectionCode")
    commodity = fields.Char(string="Commodity")
    deliveryterm = fields.Char(string="DeliveryTerm")
    strategy = fields.Char(string="Strategy")
    location = fields.Char(string="Location")
    lot = fields.Char(string="Lot")
    lotsize = fields.Char(string="LotSize")
    tradeqty = fields.Char(string="TradeQty")
    qtyuom = fields.Char(string="QtyUom")
    calendar = fields.Char(string="Calendar")
    startdate = fields.Char(string="StartDate")
    enddate = fields.Char(string="EndDate")
    deliveryschedule = fields.Char(string="DeliverySchedule")
    settlementcurrency = fields.Char(string="SettlementCurrency")
    settlementuom = fields.Char(string="SettlementUom")
    settlementpaymentterm = fields.Char(string="SettlementPaymentTerm")
    letterofcredit = fields.Char(string="LetterOfCredit")
    venturecode = fields.Char(string="VentureCode")
    logisticcontractid = fields.Char(string="LogisticContractId")
    tradelinkid = fields.Char(string="TradeLinkId")
    tradelinkcode = fields.Char(string="TradeLinkCode")
    exchangecontract = fields.Char(string="ExchangeContract")
    exchangeref = fields.Char(string="ExchangeRef")
    brokerref = fields.Char(string="BrokerRef")
    broker2company = fields.Char(string="Broker2Company")
    exchange = fields.Char(string="Exchange")
    tradeprice = fields.Char(string="TradePrice")
    pricecurrency = fields.Char(string="PriceCurrency")
    priceuom = fields.Char(string="PriceUom")
    commoditygroup = fields.Char(string="CommodityGroup")
    intercomptradenumber = fields.Char(string="InterCompTradeNumber")
    stagename = fields.Char(string="StageName")
    currentstagename = fields.Char(string="CurrentStageName")
    loadlocation = fields.Char(string="LoadLocation")
    dischargelocation = fields.Char(string="DischargeLocation")
    account = fields.Char(string="Account")
    book = fields.Char(string="Book")
    brand = fields.Char(string="Brand")
    shape = fields.Char(string="Shape")
    udf1 = fields.Char(string="Udf1")
    udf2 = fields.Char(string="Udf2")
    udf3 = fields.Char(string="Udf3")
    udf4 = fields.Char(string="Udf4")
    udf5 = fields.Char(string="Udf5")
    udf6 = fields.Char(string="Udf6")
    udf7 = fields.Char(string="Udf7")
    udf8 = fields.Char(string="Udf8")
    udf9 = fields.Char(string="Udf9")
    udf10 = fields.Char(string="Udf10")
    grade = fields.Char(string="Grade")
    fund = fields.Char(string="Fund")
    origin = fields.Char(string="Origin")
    mastercontractid = fields.Char(string="MasterContractId")
    segmentreference = fields.Char(string="SegmentReference")
    portfolio = fields.Char(string="Portfolio")
    totalallocatedqty = fields.Char(string="TotalAllocatedQty")
    openallocatedqty = fields.Char(string="OpenAllocatedQty")
    concentrateenum = fields.Char(string="ConcentrateEnum")
    qstype = fields.Char(string="QsType")
    financingaccount = fields.Char(string="FinancingAccount")
    financingtransferdate = fields.Char(string="FinancingTransferDate")
    customerreference = fields.Char(string="CustomerReference")
    businessunit = fields.Char(string="BusinessUnit")
    portfoliosegment = fields.Char(string="PortfolioSegment")
    declarationdate = fields.Char(string="DeclarationDate")
    optionalsectionenum = fields.Char(string="OptionalSectionEnum")
    tradeadmin = fields.Char(string="TradeAdmin")
    operator = fields.Char(string="Operator")
    material = fields.Char(string="Material")
    mot = fields.Char(string="Mot")
    masterdealid = fields.Char(string="MasterDealId")
    expirydate = fields.Char(string="ExpiryDate")
    linktype = fields.Char(string="LinkType")
    billtopartycounterpart = fields.Char(string="BillToPartyCounterpart")
    payercounterpart = fields.Char(string="PayerCounterpart")
    shiptopartycounterpart = fields.Char(string="ShipToPartyCounterpart")
    invoicepresentedbycounterpart = fields.Char(string="InvoicePresentedByCounterpart")
    intercompanybuyid = fields.Char(string="InterCompanyBuyId")
    intercompanysellid = fields.Char(string="InterCompanySellId")
    intercompanytemplatecode = fields.Char(string="IntercompanyTemplateCode")
    isnotforownuse = fields.Char(string="IsNotForOwnUse")
    isembeddedderivative = fields.Char(string="IsEmbeddedDerivative")
    dealsheetmasterid = fields.Char(string="DealSheetMasterId")
    internalstorage = fields.Char(string="InternalStorage")
    internalportfolio = fields.Char(string="InternalPortfolio")
    internalstrategy = fields.Char(string="InternalStrategy")
    planningquantity = fields.Char(string="PlanningQuantity")
    shippingquantity = fields.Char(string="ShippingQuantity")
    planninguom = fields.Char(string="PlanningUom")
    shippinguom = fields.Char(string="ShippingUom")
    isfinanciallysettled = fields.Char(string="IsFinanciallySettled")
    offersheetmappedtodeal = fields.Char(string="OfferSheetMappedToDeal")
    istastrade = fields.Boolean(string="IsTasTrade")
    quotestdformula = fields.Char(string="QuoteStdFormula")
    expirationdate = fields.Char(string="ExpirationDate")
    hourlydailyqty = fields.Char(string="HourlyDailyQty")
    efpdealmasterid = fields.Char(string="EfpDealMasterId")
    voyagesegmenttypeenum = fields.Char(string="VoyageSegmentTypeEnum")
    isparkandloan = fields.Boolean(string="IsParkAndLoan")
    ispool = fields.Boolean(string="IsPool")
    vesselname = fields.Char(string="VesselName")
    tradesubstatus = fields.Char(string="TradeSubStatus")
    tradetype = fields.Char(string="TradeType")
    pricingtype = fields.Char(string="PricingType")
    charteringinstrumentid = fields.Char(string="CharteringInstrumentId")
    financingbank = fields.Char(string="FinancingBank")
    mailingaddress = fields.Char(string="MailingAddress")
    shippingaddress = fields.Char(string="ShippingAddress")
    billingaddress = fields.Char(string="BillingAddress")
    referencenumber = fields.Char(string="ReferenceNumber")
    hscodetype = fields.Char(string="HsCodeType")
    companysector = fields.Char(string="CompanySector")
    internalreference = fields.Char(string="InternalReference")
    ishazardousenum = fields.Char(string="IsHazardousEnum")
    unnumber = fields.Char(string="UnNumber")
    unpackagingcode = fields.Char(string="UnPackagingCode")
    isreach = fields.Boolean(string="IsReach")
    reachregistrationno = fields.Char(string="ReachRegistrationNo")
    shelflife = fields.Char(string="ShelfLife")
    iscoacheck = fields.Boolean(string="IsCoaCheck")
    isanimalfeed = fields.Boolean(string="IsAnimalFeed")
    isvendor = fields.Boolean(string="IsVendor")
    iscustomer = fields.Boolean(string="IsCustomer")
    isserviceprovider = fields.Boolean(string="IsServiceProvider")
    isproducermanufacturing = fields.Boolean(string="IsProducerManufacturing")
    isrepackertollerer = fields.Boolean(string="IsRepackerTollerer")
    isother = fields.Boolean(string="IsOther")
    hscodegeneral = fields.Char(string="HsCodeGeneral")
    hscodelocal = fields.Char(string="HsCodeLocal")
    hscodetotal = fields.Char(string="HsCodeTotal")
    commoditygroup2 = fields.Char(string="CommodityGroup2")
    tradeinputdate = fields.Char(string="TradeInputDate")
    triggerexpirationdate = fields.Char(string="TriggerExpirationDate")
    exchcontracttype = fields.Char(string="ExchContractType")
    internalreference1 = fields.Char(string="InternalReference1")
    securityid = fields.Char(string="SecurityId")
    isfinalized = fields.Boolean(string="IsFinalized")
    istimespread = fields.Boolean(string="IsTimeSpread")
    isimportedtrade = fields.Boolean(string="IsImportedTrade")
    sectiontypeenum = fields.Char(string="SectionTypeEnum")
    finalizeddate = fields.Char(string="FinalizedDate")
    tradelastmodifieddate = fields.Char(string="TradeLastModifiedDate")
    isstructureddeal = fields.Char(string="IsStructuredDeal")
    tradestatus = fields.Char(string="TradeStatus")
    agreementtypename = fields.Char(string="AgreementTypeName")
    agreementtypecode = fields.Char(string="AgreementTypeCode")
    cropyear = fields.Char(string="CropYear")
    variety = fields.Char(string="Variety")
    contracttype = fields.Char(string="ContractType")
    isinternal = fields.Char(string="IsInternal")
    tradeblotterprocessmasterid = fields.Char(string="TradeBlotterProcessMasterId")
    asset = fields.Char(string="Asset")
    clearingbroker = fields.Char(string="ClearingBroker")
    cashbroker = fields.Char(string="CashBroker")
    vehicle = fields.Char(string="Vehicle")
    vehiclemottype = fields.Char(string="VehicleMotType")
    linespace = fields.Char(string="LineSpace")
    cleared = fields.Char(string="Cleared")
    description = fields.Char(string="Description")
    isforcemajeure = fields.Boolean(string="IsForceMajeure")
    specificationcode = fields.Char(string="SpecificationCode")
    packagingcode = fields.Char(string="PackagingCode")
    licensecode = fields.Char(string="LicenseCode")
    mtmpricingtype = fields.Char(string="MtmPricingType")
    qtyperiodicitytype = fields.Char(string="QtyPeriodicityType")
    isicedeal = fields.Boolean(string="IsIceDeal")
    companyagreementid = fields.Char(string="CompanyAgreementId")
    buysell = fields.Char(string="BuySell")
    billtolocation = fields.Char(string="BillToLocation")
    locationbsoption = fields.Char(string="LocationBsOption")
    iscallgas = fields.Boolean(string="IsCallGas")
    remaininglots = fields.Char(string="RemainingLots")
    legtype = fields.Char(string="LegType")
    weightfinalat = fields.Char(string="WeightFinalAt")
    regionlocation = fields.Char(string="RegionLocation")
    flowstartdate = fields.Char(string="FlowStartDate")
    flowenddate = fields.Char(string="FlowEndDate")
    transfernumber = fields.Char(string="TransferNumber")
    nominationkey = fields.Char(string="NominationKey")
    offernumber = fields.Char(string="OfferNumber")
    brokersubaccount = fields.Char(string="BrokerSubAccount")
    actualprice = fields.Char(string="ActualPrice")
    actualpriceuom = fields.Char(string="ActualPriceUom")
    actualpriceccy = fields.Char(string="ActualPriceCcy")
    shiptolocation = fields.Char(string="ShipToLocation")
    quote = fields.Char(string="Quote")
    servicelevelenum = fields.Char(string="ServiceLevelEnum")
    pipelineratematrix = fields.Char(string="PipelineRateMatrix")
    mtmcurve = fields.Char(string="MtmCurve")
    price = fields.Char(string="Price")
    pricingterm = fields.Char(string="PricingTerm")
    paymentterm = fields.Char(string="PaymentTerm")
    contactperson = fields.Char(string="ContactPerson")
    companyagreementtype = fields.Char(string="CompanyAgreementType")
    curvecategory = fields.Char(string="CurveCategory")
    indextype = fields.Char(string="IndexType")
    iscomposite = fields.Boolean(string="IsComposite")
    ismtmoverwrite = fields.Boolean(string="IsMtmOverwrite")
    ismtmdefault = fields.Boolean(string="IsMtmDefault")
    isattachmentavailable = fields.Char(string="IsAttachmentAvailable")
    isnotesavailable = fields.Char(string="IsNotesAvailable")
    capacityquantity = fields.Char(string="CapacityQuantity")
    strategyl1 = fields.Char(string="StrategyL1")
    strategyl2 = fields.Char(string="StrategyL2")
    strategyl3 = fields.Char(string="StrategyL3")
    strategyl4 = fields.Char(string="StrategyL4")
    strategyl5 = fields.Char(string="StrategyL5")
    customtradenumber = fields.Char(string="CustomTradeNumber")
    customsectionnumber = fields.Char(string="CustomSectionNumber")
    iscontractnotrequired = fields.Boolean(string="IsContractNotRequired")
    cpterm = fields.Char(string="CpTerm")
    segmentstatus = fields.Char(string="SegmentStatus")
    promptdate = fields.Char(string="PromptDate")
    parentlinktradeid = fields.Char(string="ParentLinkTradeId")
    lastvalueddate = fields.Char(string="LastValuedDate")
    internalbusinessunit = fields.Char(string="InternalBusinessUnit")
    isintercompanypricing = fields.Boolean(string="IsIntercompanyPricing")
    isinvoiced = fields.Boolean(string="IsInvoiced")
    productcode = fields.Char(string="ProductCode")
    fxamountcurrency = fields.Char(string="FxAmountCurrency")
    productsymbol = fields.Char(string="ProductSymbol")
    istradelock = fields.Boolean(string="IsTradeLock")
    lotequivalent = fields.Char(string="LotEquivalent")
    istermallocatedtobargefreight = fields.Boolean(string="IsTermAllocatedToBargeFreight")
    scheduleenum = fields.Char(string="ScheduleEnum")
    certificateno = fields.Char(string="CertificateNo")
    inventorytypedisplayname = fields.Char(string="InventoryTypeDisplayName")
    fileimportid = fields.Char(string="FileImportId")
    triggerallocationmethod = fields.Char(string="TriggerAllocationMethod")
    strikeprice = fields.Char(string="StrikePrice")
    hscode = fields.Char(string="HsCode")
    unallocatedlinktradeqty = fields.Char(string="UnallocatedLinkTradeQty")
    deliverybasisof = fields.Char(string="DeliveryBasisOf")
    isddp = fields.Boolean(string="IsDdp")
    putcall = fields.Char(string="PutCall")
    underlyingproductcode = fields.Char(string="UnderlyingProductCode")
    refphysicalid = fields.Char(string="RefPhysicalId")
    lockid = fields.Char(string="LockId")
    statusenum = fields.Char(string="StatusEnum")
    modifypersonid = fields.Char(string="ModifyPersonId")
    modifyperson = fields.Char(string="ModifyPerson")
    lastmodifydate = fields.Char(string="LastModifyDate")
    customerid = fields.Char(string="CustomerId")
    birecordcreationdate = fields.Char(string="BiRecordCreationDate")
    
    def import_trade(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/trade"
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
                for data in json_data:
                    self.create_update_trade('trade', data)
                interface.update_sync_interface('trade')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_trade(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('trade')
        url = "https://fusionsqlmirrorapi.azure-api.net/api/trade"
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
                for data in json_data:
                    self.regular_update_trade('trade', data)
                interface.update_sync_interface('trade')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_trade(self, interface_type, data):
        if interface_type == 'trade':
            exists = self.env['trade.controller.bi'].search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])])
            if exists:
                return
                # if exists:
                #     return
                # else:
                #     self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
                #     self.env['cashflow.controller.bi'].create(data)
                #     self.env.cr.commit()
            else:
                self.env['trade.controller.bi'].create(data)
                self.env.cr.commit()
    
    def regular_update_trade(self, interface_type, data):
        if interface_type == 'trade':
            exists = self.env['trade.controller.bi'].search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])])
            if exists:
                self.env['trade.controller.bi'].search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])]).unlink()
                self.env['trade.controller.bi'].create(data)
            else:
                self.env['trade.controller.bi'].create(data)
                self.env.cr.commit()
    
    def create_purchase_order(self):
        try:
            for rec in self.env['trade.controller.bi'].search([('id','in',self.env.context['active_ids'])]):
                if rec.buysell == 'Buy':
                    existing_po = self.env['purchase.order'].search([('fusion_deal_number', '=', rec.dealmasterid)])
                    if existing_po:
                        # code for existing PO
                        a = 1
                    else:
                        partner = self.env['res.partner'].search([('name', '=', rec.counterpartcompany)], limit=1)
                        
                        currency = self.env['res.currency'].search([('name', '=', rec.settlementcurrency)], limit=1)
                        company = self.env['res.company'].search([('name', '=', rec.internalcompany)], limit=1)
                        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company.id)],limit=1)

                        location = self.env['incoterm.location'].search([('name', '=', rec.location)],limit=1)
                        if not location:
                            location = self.env['incoterm.location'].create({
                                'name' : rec.location
                            })
                        # company=
                        # match rec.internalcompany:
                        #     case 'KEMEXON LTD':
                        #         company= 1
                        #     case "KEMEXON SA":
                        #         company= 2
                        #     case "KEMEXON BELGIUM SRL":
                        #         company= 4
                            
                        if partner:
                            
                            all_segments = self.env['trade.controller.bi'].search(
                                [('dealmasterid', '=', rec.dealmasterid)])
                            lines = []
                            for segment in all_segments:
                                product = self.env['product.template'].search([('name', '=', segment.material)], limit=1)
                                trade_uom = self.env['uom.uom'].search([('category_id', '=', product.uom_id.category_id.id), ('name', '=', segment.qtyuom)])
                                uom = ''
                                incoterm = self.env['account.incoterms'].search([('name','=',rec.deliveryterm)])
                                if trade_uom:
                                    uom = trade_uom.id
                                else:
                                    uom = self.env['uom.uom'].create({
                                        'name': segment.qtyuom,
                                        'category_id': product.uom_id.category_id.id,
                                        'ratio': 1
                                    })
                                lines.append((0, 0, {
                                    'product_id': product.id,
                                    'name': product.name + segment.shape if segment.shape else product.name,
                                    'sh_warehouse_id': warehouse.id,
                                    'product_qty': segment.tradeqty if Decimal(segment.tradeqty) >= 0 else segment.tradeqty*-1,
                                    'product_uom': uom,
                                    'price_unit': float(segment.price) if self.is_convertible_to_float(segment.price)  else 0
                                }))
                            deal = {
                                'currency_id': currency.id,
                                'partner_id': partner.id,
                                'partner_ref': rec.description,
                                'company_id': company.id,
                                'incoterm_id': incoterm.id,
                                'date_approve': datetime.datetime.strptime(rec.tradedate, '%Y-%m-%dT%H:%M:%S'),
                                'incoterm_location_custom': location.id,
                                'fusion_deal_number' :rec.dealmasterid
                                
                            }
                            deal['order_line'] = lines
                            purchase_order = self.env['purchase.order'].create(deal)
                
        except Exception as e:
            raise UserError('Error processing API data: %s', str(e))
    
    def is_convertible_to_float(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False