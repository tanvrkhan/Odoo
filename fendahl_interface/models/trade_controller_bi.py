from odoo import models, fields
import requests
import logging
import datetime
from odoo.exceptions import UserError, Warning
from decimal import Decimal
_logger = logging.getLogger(__name__)
from dateutil import parser
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
                self.regular_update_trade('trade', json_data)
                interface.update_sync_interface('trade')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def process_odoo_transaction_action(self):
        interface = self.env['fusion.sync.history']
        last_processing_date = interface.get_last_processing('trade')
        trades_to_process =  self.env['trade.controller.bi'].search([('lastmodifydate','>=',last_processing_date)])
        for rec in trades_to_process:
            if rec.internalcompany == 'KEMEXON LTD' or  rec.internalcompany == 'KEMEXON SA':
                rec.create_order()
        interface.update_processing_date('trade')
    
    def sync_trade(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('trade')
        max_synced_date = self.env['trade.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                        order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
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
                self.regular_update_trade('trade', json_data)
                interface.update_sync_interface('trade')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_trade(self, interface_type, json_data):
        if interface_type == 'trade':
            all = self.env['trade.controller.bi'].search([])
            if all:
                for data in json_data:
                    exists = all.search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])])
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
            else:
                for data in json_data:
                    self.env['trade.controller.bi'].create(data)
                    self.env.cr.commit()
                
    
    def regular_update_trade(self, interface_type, json_data):
        if interface_type == 'trade':
            all = self.env['trade.controller.bi'].search([])
            for data in json_data:
                exists = all.search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])])
                if exists:
                    self.env['trade.controller.bi'].search([('dealmasterid', '=', data['dealmasterid']),('segmentid', '=', data['segmentid'])]).unlink()
                    self.env['trade.controller.bi'].create(data)
                else:
                    self.env['trade.controller.bi'].create(data)
                    self.env.cr.commit()
    
    
    def validate_payment_term(self,settlementpaymentterm):
        if settlementpaymentterm:
            payment_term = self.env['account.payment.term'].search([('name', '=', settlementpaymentterm)])
            if not payment_term:
                payment_term = self.env['account.payment.term'].create({
                    'name': settlementpaymentterm
                })
            return payment_term
        else:
            return
    def validate_incoterm_location(self,locationname):
        if locationname:
            location = self.env['incoterm.location'].search([('name', '=', locationname)], limit=1)
            if not location:
                location = self.env['incoterm.location'].create({
                    'name': locationname
                })
            return location
        else:
            return
    def get_triggered_price(self, rec):
        if rec.pricingtype == 'Fixed':
            return float(rec.price)
        else:
            cashflow_lines = self.env['cashflow.controller.bi'].read_group(
                domain=[('quantitystatus', '=', 'Actual'),('sectionno', '=', rec.segmentsectioncode),('costtype', '=', "Primary Settlement"),('actualestimate', '=', "Actual"),('cashflowstatus', '=', "Active")],
                fields=['price:avg'],
                # Fields to load
                groupby=['quantitystatus', 'sectionno', 'costtype', 'actualestimate'],
                lazy=False  # Get results for each partner directly
            )
            if not cashflow_lines:
                cashflow_lines = self.env['cashflow.controller.bi'].read_group(
                    domain=[('quantitystatus', '=', 'Actual'), ('sectionno', '=', rec.segmentsectioncode),
                            ('costtype', '=', "Primary Settlement"),
                            ('cashflowstatus', '=', "Active")],
                    fields=['price:avg'],
                    # Fields to load
                    groupby=['quantitystatus', 'sectionno', 'costtype', 'actualestimate'],
                    lazy=False  # Get results for each partner directly
                )
                if not cashflow_lines:
                    cashflow_lines = self.env['cashflow.controller.bi'].read_group(
                        domain=[('quantitystatus', '=', 'Contractual'), ('sectionno', '=', rec.segmentsectioncode),
                                ('costtype', '=', "Primary Settlement"),
                                ('cashflowstatus', '=', "Active")],
                        fields=['price:avg'],
                        # Fields to load
                        groupby=['quantitystatus', 'sectionno', 'costtype', 'actualestimate'],
                        lazy=False  # Get results for each partner directly
                    )
               
                    
            if cashflow_lines:
                return round(cashflow_lines[0]['price'],2)
            else:
                return 0
    def update_order(self,type,existing_order,rec,currency,partner,incoterm,location,payment_term):
        company = self.env['res.company'].search([('name', '=', rec.internalcompany)],
                                                 limit=1)

        warehouse = self.env['fusion.sync.history'].validate_warehouse(rec.location,company)
        if type=='Purchase Order':
            existing_order.write({'date_approve': datetime.datetime.strptime(
                                                    rec.tradedate, '%Y-%m-%dT%H:%M:%S')})
            existing_order.write({'currency_id': currency.id})
            existing_order.write({'partner_id': partner.id})
            existing_order.write({'partner_ref': rec.description})
            existing_order.write({'incoterm_id': incoterm.id})
            existing_order.write({'incoterm_location_custom': location.id})
            existing_order.write({'fusion_deal_number': rec.dealmasterid})
            existing_order.write({'payment_term_id': payment_term.id})
            self.update_po_lines(existing_order,rec,company,warehouse)
        elif type=='Sale Order':
            pricelist = self.env['product.pricelist'].search([('currency_id', '=', currency.id),('company_id', '=', False)], limit=1)
            existing_order.write({'pricelist_id': pricelist.id})
            existing_order.write({'partner_id': partner.id})
            existing_order.write({'deal_ref': rec.description})
            existing_order.write({'date_order': datetime.datetime.strptime(
                                                    rec.tradedate, '%Y-%m-%dT%H:%M:%S')})
            existing_order.write({'incoterm': incoterm.id})
            existing_order.write({'incoterm_location_custom': location.id})
            existing_order.write({'fusion_deal_number': rec.dealmasterid})
            existing_order.write({'payment_term_id': payment_term.id})
            self.update_so_lines(existing_order, rec, company, warehouse)
    def update_po_lines(self,existing_order,rec,company,warehouse):
        all_segments = self.env['trade.controller.bi'].search(
            [('dealmasterid', '=', rec.dealmasterid)])
        lines = []
        for segment in all_segments:
            main_cf = cf = self.env['cashflow.controller.bi'].search(
                [('sectionno', '=', segment.segmentsectioncode), ('costtype', '=', 'Primary Settlement')], limit=1)
            tax_cf = self.env['cashflow.controller.bi'].search(
                [('parentcashflowid', '=', main_cf.cashflowid), ('costtype', '=', 'VAT')], limit=1)
            tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode,
                                                                             'purchase', company.id)
            existing_line  = existing_order.order_line.filtered(
                lambda ol: ol.fusion_segment_code == segment.segmentsectioncode)
            if existing_line:
                existing_line.price_unit = self.get_triggered_price(segment)
                continue
            else:
                self.create_new_po_line(existing_order,segment,warehouse,company,tax_rate_record)
                
    def update_so_lines(self, existing_order, rec, company, warehouse):
        all_segments = self.env['trade.controller.bi'].search(
            [('dealmasterid', '=', rec.dealmasterid)])
        lines = []
        for segment in all_segments:
            main_cf = cf = self.env['cashflow.controller.bi'].search(
                [('sectionno', '=', segment.segmentsectioncode), ('costtype', '=', 'Primary Settlement')],
                limit=1)
            tax_cf = self.env['cashflow.controller.bi'].search(
                [('parentcashflowid', '=', main_cf.cashflowid), ('costtype', '=', 'VAT')], limit=1)
            tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode,
                                                                             'sale', company.id)
            existing_line = existing_order.order_line.filtered(
                    lambda ol: ol.fusion_segment_code == segment.segmentsectioncode)
            if existing_line:
                existing_line.price_unit = self.get_triggered_price(segment)
                continue
            else:
                self.create_new_so_line(existing_order, segment, warehouse, company, tax_rate_record)
    def create_new_po_line(self,existing_po,segment,warehouse,company,tax_rate_record):
        product = self.env['fusion.sync.history'].validate_product(segment.commodity,
                                                                   segment.material,
                                                                   segment.qtyuom)
        if product:
            uom = self.env['fusion.sync.history'].validate_uom(product, segment.qtyuom)
            
            commodity_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Commodity',
                                                                                   segment.commodity,
                                                                                   company.id)
            trader_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Trader',
                                                                                segment.traderperson,
                                                                                company.id)
            strategy_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Strategy',
                                                                                  segment.strategy,
                                                                                  company.id)
            
            price = self.get_triggered_price(segment)
            analytic_distribution={}
            if commodity_ann:
                analytic_distribution[commodity_ann.id] = 100
            if trader_ann:
                analytic_distribution[trader_ann.id] = 100
            if strategy_ann:
                analytic_distribution[strategy_ann.id] = 100
            line = {
                'product_id': product.id,
                'name': product.name + segment.shape if segment.shape else product.name,
                'sh_warehouse_id': warehouse.id,
                'product_qty': segment.tradeqty if Decimal(
                    segment.tradeqty) >= 0 else segment.tradeqty * -1,
                'product_uom': uom.id,
                'price_unit': float(price) if self.is_convertible_to_float(price) else segment.price,
                'analytic_distribution': analytic_distribution,
                #     'analytic_distribution': {
                #     commodity_ann.id: 100,
                #     trader_ann.id: 100,
                #     strategy_ann.id: 100,
                #     # portfolio_ann.id: 100,
                # },
                'taxes_id': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])],
                'fusion_segment_id': segment.segmentid,
                'custom_section_number': segment.customsectionnumber,
                'fusion_segment_code': segment.segmentsectioncode
            }
            existing_po.write({
                'order_line': [(0, 0, line)]
            })
    
    def create_new_so(self, rec, warehouse, company, partner, incoterm, location, payment_term, currency):
        
        all_segments = self.env['trade.controller.bi'].search(
            [('dealmasterid', '=', rec.dealmasterid)])
        lines = []
        pricelist = self.env['product.pricelist'].search(
            [('currency_id', '=', currency.id), ('company_id', '=', False)], limit=1)
        for segment in all_segments:
            main_cf = cf = self.env['cashflow.controller.bi'].search(
                [('sectionno', '=', segment.segmentsectioncode)], limit=1)
            tax_cf = self.env['cashflow.controller.bi'].search(
                [('parentcashflowid', '=', main_cf.cashflowid), ('costtype', '=', 'VAT')], limit=1)
            tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode,
                                                                             'sale', company.id)
            product = self.env['fusion.sync.history'].validate_product(segment.commodity, segment.material,
                                                                       segment.qtyuom)
            if product:
                uom = self.env['fusion.sync.history'].validate_uom(product, segment.qtyuom)
                
                commodity_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Commodity', segment.commodity,
                                                                                       company.id)
                trader_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Trader', segment.traderperson,
                                                                                    company.id)
                strategy_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Strategy', segment.strategy,
                                                                                      company.id)
                analytic_distribution = {}
                if commodity_ann:
                    analytic_distribution[commodity_ann.id] = 100
                if trader_ann:
                    analytic_distribution[trader_ann.id] = 100
                if strategy_ann:
                    analytic_distribution[strategy_ann.id] = 100
                # portfolio_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Portfolio', segment.portfoliosegment, company.id)
                price = self.get_triggered_price(segment)
                lines.append((0, 0, {
                    'product_id': product.id,
                    'name': product.name + segment.shape if segment.shape else product.name,
                    # 'sh_warehouse_id': warehouse.id,
                    'product_uom_qty': segment.tradeqty if float(segment.tradeqty) >= 0 else float(segment.tradeqty) * -1,
                    'product_uom': uom.id,
                    'price_unit': float(price) if self.is_convertible_to_float(price) else segment.price,
                    'analytic_distribution': analytic_distribution,
                    'tax_id': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])],
                    'fusion_segment_id': segment.segmentid,
                    'custom_section_number': segment.customsectionnumber,
                    'fusion_segment_code': segment.segmentsectioncode,
                    
                }))
            else:
                log_error = self.env['fusion.sync.history.errors'].log_error('TradeControllerBI',
                                                                             rec.segmentid,
                                                                             'Product not found',
                                                                             segment.internalcompany)
        deal = {
            'pricelist_id': pricelist.id,
            'partner_id': partner.id,
            'deal_ref': rec.description,
            'company_id': company.id,
            'incoterm': incoterm.id,
            # 'date_approve': datetime.datetime.strptime(rec.tradedate, '%Y-%m-%dT%H:%M:%S'),
            'date_order': rec.tradedate.replace('T', ' '),
            'incoterm_location_custom': location.id,
            'fusion_deal_number': rec.dealmasterid,
            'payment_term_id': payment_term.id,
            
        }
        deal['order_line'] = lines
        so = self.env['sale.order'].create(deal)
        self.env.cr.commit()
    def create_new_so_line(self, existing_order, segment, warehouse, company, tax_rate_record):
        product = self.env['fusion.sync.history'].validate_product(segment.commodity,
                                                                   segment.material,
                                                                   segment.qtyuom)
        if product:
            uom = self.env['fusion.sync.history'].validate_uom(product, segment.qtyuom)
            
            commodity_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Commodity',
                                                                                   segment.commodity,
                                                                                   company.id)
            trader_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Trader',
                                                                                segment.traderperson,
                                                                                company.id)
            strategy_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Strategy',
                                                                                  segment.strategy,
                                                                                  company.id)
            analytic_distribution = {}
            if commodity_ann:
                analytic_distribution[commodity_ann.id] = 100
            if trader_ann:
                analytic_distribution[trader_ann.id] = 100
            if strategy_ann:
                analytic_distribution[strategy_ann.id] = 100
            price = self.get_triggered_price(segment)
            line = {
                'product_id': product.id,
                'name': product.name + segment.shape if segment.shape else product.name,
                # 'sh_warehouse_id': warehouse.id,
                'product_uom_qty': segment.tradeqty if Decimal(
                    segment.tradeqty) >= 0 else segment.tradeqty * -1,
                'product_uom': uom.id,
                'price_unit': float(price) if self.is_convertible_to_float(price) else 0,
                'analytic_distribution': analytic_distribution,
                'tax_id': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])],
                'fusion_segment_id': segment.segmentid,
                'custom_section_number': segment.customsectionnumber,
                'fusion_segment_code': segment.segmentsectioncode
            }
            existing_order.write({
                'order_line': [(0, 0, line)]
            })
            
    def create_new_po(self,rec,warehouse,company,partner,incoterm,location,payment_term,currency):
        
        all_segments = self.env['trade.controller.bi'].search(
            [('dealmasterid', '=', rec.dealmasterid)])
        lines = []
        for segment in all_segments:
            main_cf = self.env['cashflow.controller.bi'].search(
                [('sectionno', '=', segment.segmentsectioncode),('costtype', '=', "Primary Settlement")], limit=1)
            tax_cf = self.env['cashflow.controller.bi'].search(
                [('parentcashflowid', '=', main_cf.cashflowid), ('costtype', '=', 'VAT')], limit=1)
            tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode,
                                                                             'purchase', company.id)
            product = self.env['fusion.sync.history'].validate_product(segment.commodity, segment.material,
                                                                       segment.qtyuom)
            if product:
                uom = self.env['fusion.sync.history'].validate_uom(product, segment.qtyuom)
                
                commodity_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Commodity', segment.commodity,
                                                                                       company.id)
                trader_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Trader', segment.traderperson,
                                                                                    company.id)
                strategy_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Strategy', segment.strategy,
                                                                                      company.id)
                analytic_distribution = {}
                if commodity_ann:
                    analytic_distribution[commodity_ann.id] = 100
                if trader_ann:
                    analytic_distribution[trader_ann.id] = 100
                if strategy_ann:
                    analytic_distribution[strategy_ann.id] = 100
                # portfolio_ann = self.env['fusion.sync.history'].checkAndDefineAnalytic('Portfolio', segment.portfoliosegment, company.id)
                
                lines.append((0, 0, {
                    'product_id': product.id,
                    'name': product.name + segment.shape if segment.shape else product.name,
                    'sh_warehouse_id': warehouse.id,
                    'product_qty': segment.tradeqty if Decimal(segment.tradeqty) >= 0 else segment.tradeqty * -1,
                    'product_uom': uom.id,
                    'price_unit': self.get_triggered_price(segment),
                    'analytic_distribution': analytic_distribution,
                    'taxes_id': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])],
                    'fusion_segment_id': segment.segmentid,
                    'custom_section_number': segment.customsectionnumber,
                    'fusion_segment_code': segment.segmentsectioncode,
                    
                }))
            else:
                log_error = self.env['fusion.sync.history.errors'].log_error('TradeControllerBI',
                                                                             rec.segmentid,
                                                                             'Product not found',
                                                                             segment.internalcompany)
        deal = {
            'currency_id': currency.id,
            'partner_id': partner.id,
            'partner_ref': rec.description,
            'company_id': company.id,
            'incoterm_id': incoterm.id,
            'date_approve': datetime.datetime.strptime(rec.tradedate, '%Y-%m-%dT%H:%M:%S'),
            'date_order': datetime.datetime.strptime(rec.tradedate, '%Y-%m-%dT%H:%M:%S'),
            'incoterm_location_custom': location.id,
            'fusion_deal_number': rec.dealmasterid,
            'payment_term_id': payment_term.id,
            
        }
        deal['order_line'] = lines
        po = purchase_order = self.env['purchase.order'].create(deal)
        
            
        self.env.cr.commit()
    
    def do_interco_transfers(self):
        for rec in self:
            all_segments = self.env['trade.controller.bi'].search(
                [('dealmasterid', '=', rec.dealmasterid)])
            for interco_trade in all_segments.filtered(
                    lambda ml: ml.tradeprice == "Intercompany Trade"):
                rec.check_confirm_transfer(interco_trade)
                
                
    def create_move_for_picking(self,picking, product, quantity,sol):
      stock_move = self.env['stock.move'].create({
          'name': product.display_name,
          'product_id': product.id,
          'product_uom_qty': quantity,
          'product_uom': product.uom_id.id,
          'location_id': picking.location_id.id,
          'location_dest_id': picking.location_dest_id.id,
          'picking_id': picking.id,
          'sale_line_id': sol.id,
      })
      return stock_move
    def check_confirm_transfer(self,segment):
        transfers = self.evnv['stock.picking'].search([('fusion_segment_code', '=', segment.segmentsectioncode)])
        if segment.tradeprice == "Intercompany Trade":
            company = self.env['res.company'].search([('name', '=', segment.internalcompany)],
                                                     limit=1)
            warehouse = self.env['fusion.sync.history'].validate_warehouse(segment.location,
                                                                           company)
            sol =  self.env['sale.order.line']
            pol =  self.env['purchase.order.line']
            picking = self.env['stock.picking']
            picking_type = self.env['stock.picking.type']
            stock_move =  self.env['stock.move']
            
            existing_move = self.env['stock.move'].search([('fusion_segment_code', '=', segment.segmentsectioncode)])
            if existing_move:
                pol = self.env['purchase.order.line'].search(
                    [('fusion_segment_code', '=', segment.segmentsectioncode)], limit=1)
                sol = self.env['sale.order.line'].search([('fusion_segment_code', '=', segment.segmentsectioncode)],
                                                         limit=1)
                if existing_move.fusion_last_modify == self.parse_datetime(segment.lastmodifydate) and existing_move.state == 'done':
                    return
                else:
                    existing_move.fusion_segment_code = segment.segmentsectioncode
                    existing_move.fusion_last_modify = self.parse_datetime(segment.lastmodifydate)
                    picking = existing_move.picking_id
                    if picking.state in ('done', 'waiting', 'confirmed', 'cancel'):
                        picking.set_stock_move_to_draft()
                        picking.action_confirm()
                    self.update_existing_lines(existing_move, pol.product_id if pol else sol.product_id, segment, company, picking.location_id,
                                               picking.location_dest_id)
                    self.confirm_picking(picking)
                  
                    if sol:
                        sol.order_id.picking_ids = [(4, picking.id,0)]
                    if pol:
                        pol.order_id.picking_ids = [(4, picking.id,0)]
            else:
                if segment.buysell == 'Buy':
                    pol = self.env['purchase.order.line'].search([('fusion_segment_code', '=', segment.segmentsectioncode)],limit=1)
                    if pol:
                        if not pol.order_id.state == 'purchase':
                            pol.order_id.button_confirm()
                        res = pol.order_id._prepare_picking()
                        picking = self.env['stock.picking'].create(res)
                        stock_move = pol._create_stock_moves(picking[0])
                        picking_type = self.env['stock.picking.type'].search(
                            [('code', '=', 'incoming'), ('warehouse_id', '=', warehouse.id)], limit=1)
                        picking.custom_delivery_date = pol.date_approve
                        picking.scheduled_date = picking.custom_delivery_date
                        picking.date_done = picking.custom_delivery_date
                  
                elif segment.buysell == 'Sell':
                    sol = self.env['sale.order.line'].search([('fusion_segment_code', '=', segment.segmentsectioncode)],
                                                                 limit=1)
                    if sol:
                        picking_type = self.env['stock.picking.type'].search(
                            [('code', '=', 'outgoing'), ('warehouse_id', '=', warehouse.id)], limit=1)
                        if not sol.order_id.state == 'sale':
                            sol.order_id.action_confirm()
                        res = {
                            'partner_id': sol.order_id.partner_id.id,
                            'date': sol.order_id.date_order,
                            'origin': sol.order_id.name,
                            'picking_type_id': picking_type.id,
                            'sale_id': sol.order_id.id,
                        }
                        picking = self.env['stock.picking'].create(res)
                        picking.custom_delivery_date = pol.date_order
                        picking.scheduled_date = picking.custom_delivery_date
                        picking.date_done = picking.custom_delivery_date
                        stock_move = self.create_move_for_picking(picking, sol.product_id, 0,sol)
                        # stock_move = sol._create_stock_moves(picking[0])

                 
                if stock_move and (pol or sol):
                    stock_move.fusion_last_modify = self.parse_datetime(segment.lastmodifydate)
                    picking.fusion_segment_code = segment.segmentsectioncode
                    stock_move.fusion_segment_code = segment.segmentsectioncode

                    
                    product =  sol.product_id if sol else pol.product_id
                    # if stock_move and (stock_move.fusion_last_modify != self.parse_datetime(
                    #         segment.lastmodifydate) or stock_move.state != 'done'):
                    picking = stock_move.picking_id
                    stock_move.fusion_last_modify = self.parse_datetime(segment.lastmodifydate)
                    if product.uom_id.rounding != 0.001:
                        product.uom_id.rounding = 0.001
                    
                    picking.fusion_itinerary_id = segment.segmentsectioncode + 'Interco'
                    
                    if stock_move.state in ('done', 'waiting', 'confirmed', 'assigned'):
                        stock_move.picking_id.set_stock_move_to_draft()
                    # stock_move.picking_id.deal_ref = 'moved_to_Draft'
                    
                    picking.picking_type_id = picking_type
                    
                    self.update_existing_lines(stock_move, sol.product_id if sol else pol.product_id, segment, company, picking.location_id, picking.location_dest_id)
                    self.confirm_picking(picking)
                    if sol:
                        sol.order_id.picking_ids = [(4, picking.id,0)]
                    if pol:
                        pol.order_id.picking_ids = [(4, picking.id,0)]
    
    def update_existing_lines(self, stock_move, product, segment, company, fromlocation, destlocation):
        lot = self.env['fusion.sync.history'].validate_lot(segment.segmentsectioncode, product.id,
                                                           company.id)
        quantity = float(segment.tradeqty) if float(segment.tradeqty)>=0 else float(segment.tradeqty)*-1
        existing_line = stock_move.move_line_ids
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
                            line2.fusion_delivery_id = segment.segmentsectioncode
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
                    'fusion_delivery_id': segment.segmentsectioncode,
                    'company_id': company.id
                })
    def confirm_picking(self, picking):
        a = 1
        # picking.button_validate()
        # if picking.state != 'done':
        #     picking._action_done()
        # self.env.cr.commit()
    
    def parse_datetime(self, time_str):
        try:
            # First try parsing with fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            # If it fails, try parsing without fractional seconds
            return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
    def get_status(self,rec):
        status = ''
        if rec.tradestatus == 'Confirmed':
            status = 'confirm'
        elif rec.tradestatus == 'Pending':
            status = 'draft'
        elif rec.tradestatus == 'Rejected' or rec.tradestatus == 'Void':
            status = 'cancel'
        return status

        
    def create_order(self):
        for rec in self:
            try:
                status = self.get_status(rec)
                partner = self.env['res.partner'].search([('name', '=', rec.counterpartcompany)], limit=1)
                if not partner:
                    partner_info = self.env['fusion.sync.history'].get_partner_info(rec.counterpartcompany)
                    if partner_info:
                        partner = self.env['res.partner'].search([('short_name', '=', partner_info['configCode'])],
                                              limit=1)
                if not partner:
                    raise UserError("Couldn't find partner in Odoo.")
                    
                #validation if partner still doesn't exist.
                currency = self.env['res.currency'].search([('name', '=', rec.settlementcurrency)], limit=1)
                company = self.env['res.company'].search([('name', '=', rec.internalcompany)], limit=1)
                warehouse = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
                incoterm = self.env['account.incoterms'].search([('name', '=', rec.deliveryterm)])
                payment_term = self.validate_payment_term(rec.settlementpaymentterm)
                location =self.validate_incoterm_location(rec.location)
                if rec.buysell == 'Buy':
                    existing_po = self.env['purchase.order'].search([('fusion_deal_number', '=', rec.dealmasterid)])
                    if existing_po:
                        if status == 'cancel':
                            existing_po.button_cancel()
                        else:
                            self.update_order('Purchase Order',existing_po,rec,currency,partner,incoterm,location,payment_term)
                            # self.do_interco_transfers()
                    else:
                        if partner and company:
                            self.create_new_po(rec,warehouse,company,partner,incoterm,location,payment_term,currency)
                            # self.do_interco_transfers()
                            if status == 'cancel':
                                existing_po.button_cancel()
                        else:
                            log_error = self.env['fusion.sync.history.errors'].log_error('TradeControllerBI', rec.segmentid, 'Partner or Company not found',rec.internalcompany)
                if rec.buysell == 'Sell':
                    existing_so = self.env['sale.order'].search([('fusion_deal_number', '=', rec.dealmasterid)])
                    if existing_so:
                        self.update_order('Sale Order',existing_so,rec,currency,partner,incoterm,location,payment_term)
                        # self.do_interco_transfers()
                        if status == 'cancel':
                            existing_so.action_cancel()
                    else:
                        if partner and company:
                            self.create_new_so(rec,warehouse,company,partner,incoterm,location,payment_term,currency)
                            # self.do_interco_transfers()
                            if status == 'cancel':
                                existing_so.action_cancel()
                        else:
                            log_error = self.env['fusion.sync.history.errors'].log_error('TradeControllerBI', rec.segmentid, 'Partner or Company not found',rec.internalcompany)
            except Exception as e:
                log_error = self.env['fusion.sync.history.errors'].log_error('TradeControllerBI', rec.segmentid,
                                                                         'Partner or Company not found',
                                                                         rec.internalcompany)
                raise UserError('Error processing API data: %s', str(e))
    
    def is_convertible_to_float(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    