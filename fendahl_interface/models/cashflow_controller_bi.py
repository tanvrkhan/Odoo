from odoo import models, fields, api
import requests
import logging
import datetime

_logger = logging.getLogger(__name__)

class CashflowControllerBi(models.Model):
    _name = 'cashflow.controller.bi'
    _description = 'Cashflow Controller BI'
    
    cashflowbiid = fields.Integer(string='cashflowbiid')
    cashflowid = fields.Integer(string='cashflowid')
    tradenumber = fields.Integer(string='tradenumber')
    termnumber = fields.Integer(string='termnumber')
    sectionno = fields.Char(string='sectionno')
    externalreference = fields.Char(string='externalreference')
    internalreference = fields.Char(string='internalreference')
    exchangeid = fields.Char(string='exchangeid')
    brokerref = fields.Char(string='brokerref')
    strategy = fields.Char(string='strategy')
    counterpart = fields.Char(string='counterpart')
    internalcompany = fields.Char(string='internalcompany')
    underlyingstart = fields.Date(string='underlyingstart')
    underlyingend = fields.Date(string='underlyingend')
    paymentduedate = fields.Date(string='paymentduedate')
    quantity = fields.Float(string='quantity')
    quantityuom = fields.Char(string='quantityuom')
    price = fields.Float(string='price')
    pricecurrency = fields.Char(string='pricecurrency')
    priceuom = fields.Char(string='priceuom')
    extendedamount = fields.Float(string='extendedamount')
    commodity = fields.Char(string='commodity')
    tradetype = fields.Char(string='tradetype')
    costtype = fields.Char(string='costtype')
    cashflowstatus = fields.Char(string='cashflowstatus')
    tradepricingstatus = fields.Char(string='tradepricingstatus')
    priceentrystartdate = fields.Date(string='priceentrystartdate')
    priceentryenddate = fields.Date(string='priceentryenddate')
    pricingquote = fields.Char(string='pricingquote')
    price1 = fields.Float(string='price1')
    location = fields.Char(string='location')
    quantitystatus = fields.Char(string='quantitystatus')
    buysell = fields.Char(string='buysell')
    venture = fields.Char(string='venture')
    paymentstatus = fields.Char(string='paymentstatus')
    invoicenumber = fields.Integer(string='invoicenumber')
    iteminvoiced = fields.Char(string='iteminvoiced')
    financialcreditinstrument = fields.Char(string='financialcreditinstrument')
    deliveryref = fields.Char(string='deliveryref')
    deliverytype = fields.Char(string='deliverytype')
    transfernumber = fields.Integer(string='transfernumber')
    actualestimate = fields.Char(string='actualestimate')
    effectivedate = fields.Date(string='effectivedate')
    actperiod = fields.Char(string='actperiod')
    bldate = fields.Date(string='bldate')
    incoterm = fields.Char(string='incoterm')
    premdesc = fields.Float(string='premdesc')
    traderperson = fields.Char(string='traderperson')
    segmentpriceentryid = fields.Integer(string='segmentpriceentryid')
    costrevenue = fields.Char(string='costrevenue')
    pricingtype = fields.Char(string='pricingtype')
    pricecategory = fields.Char(string='pricecategory')
    payablereceivable = fields.Char(string='payablereceivable')
    strategycostnumber = fields.Integer(string='strategycostnumber')
    externalcostcategory = fields.Char(string='externalcostcategory')
    internalcostcategory = fields.Char(string='internalcostcategory')
    bucompany = fields.Char(string='bucompany')
    qualityspectype = fields.Char(string='qualityspectype')
    logisticcontractnumber = fields.Integer(string='logisticcontractnumber')
    loadlocation = fields.Char(string='loadlocation')
    dischargelocation1 = fields.Char(string='dischargelocation1')
    finaldestination = fields.Char(string='finaldestination')
    price2 = fields.Float(string='price2')
    contractqty = fields.Float(string='contractqty')
    contractqtyuom = fields.Char(string='contractqtyuom')
    loadblquantity = fields.Float(string='loadblquantity')
    loadqtyuom = fields.Char(string='loadqtyuom')
    dischargeqty1 = fields.Float(string='dischargeqty1')
    dischargeqtyuom1 = fields.Char(string='dischargeqtyuom1')
    nordate1 = fields.Date(string='nordate1')
    tradingroute = fields.Char(string='tradingroute')
    discharge2qty = fields.Float(string='discharge2qty')
    discharge2qtyuom = fields.Char(string='discharge2qtyuom')
    nordate2 = fields.Date(string='nordate2')
    discharge2locationcode = fields.Char(string='discharge2locationcode')
    costdiscription = fields.Char(string='costdiscription')
    finalquantity = fields.Float(string='finalquantity')
    finalquantityuom = fields.Char(string='finalquantityuom')
    exchangecontract = fields.Char(string='exchangecontract')
    executionbroker = fields.Char(string='executionbroker')
    marketexchange = fields.Char(string='marketexchange')
    storage = fields.Char(string='storage')
    level = fields.Char(string='level')
    retrievedate = fields.Date(string='retrievedate')
    tradedate = fields.Date(string='tradedate')
    linknumber = fields.Integer(string='linknumber')
    shape = fields.Char(string='shape')
    brand = fields.Char(string='brand')
    origin = fields.Char(string='origin')
    formulaexpression = fields.Char(string='formulaexpression')
    deliveryreference = fields.Char(string='deliveryreference')
    trailernumber = fields.Char(string='trailernumber')
    packagecount = fields.Integer(string='packagecount')
    shapecode = fields.Char(string='shapecode')
    seglotreference = fields.Char(string='seglotreference')
    book = fields.Char(string='book')
    promptdate = fields.Date(string='promptdate')
    originalextendedamt = fields.Float(string='originalextendedamt')
    costgroup = fields.Integer(string='costgroup')
    concentratetype = fields.Integer(string='concentratetype')
    titletransferdate = fields.Date(string='titletransferdate')
    allocationnumber = fields.Integer(string='allocationnumber')
    issplitcashflow = fields.Char(string='issplitcashflow')
    sourcecashflownumber = fields.Integer(string='sourcecashflownumber')
    costpercentage = fields.Float(string='costpercentage')
    franchisepercentage = fields.Float(string='franchisepercentage')
    paymentdate = fields.Date(string='paymentdate')
    paymentdescription = fields.Char(string='paymentdescription')
    logistictype = fields.Integer(string='logistictype')
    itineraryid = fields.Integer(string='itineraryid')
    frontbackleg = fields.Char(string='frontbackleg')
    storagecosttype = fields.Char(string='storagecosttype')
    storagecostnumber = fields.Integer(string='storagecostnumber')
    businessunit = fields.Char(string='businessunit')
    portfoliosegment = fields.Char(string='portfoliosegment')
    optionalsection = fields.Char(string='optionalsection')
    declarationdate = fields.Date(string='declarationdate')
    tradeadmin = fields.Char(string='tradeadmin')
    operatorperson = fields.Char(string='operatorperson')
    valuationcategory = fields.Char(string='valuationcategory')
    material = fields.Char(string='material')
    tradestatus = fields.Char(string='tradestatus')
    materialtype = fields.Char(string='materialtype')
    linktype = fields.Char(string='linktype')
    commencementdate = fields.Date(string='commencementdate')
    documentreceiptdate = fields.Date(string='documentreceiptdate')
    billtoparty = fields.Char(string='billtoparty')
    payer = fields.Char(string='payer')
    shiptoparty = fields.Char(string='shiptoparty')
    invoicepresentedby = fields.Char(string='invoicepresentedby')
    proforma = fields.Char(string='proforma')
    notforownuse = fields.Char(string='notforownuse')
    embeddedderivative = fields.Char(string='embeddedderivative')
    adjustedduedate = fields.Date(string='adjustedduedate')
    originalquantity = fields.Float(string='originalquantity')
    parentlinktradeid = fields.Integer(string='parentlinktradeid')
    internalstrategy = fields.Char(string='internalstrategy')
    internalportfolio = fields.Char(string='internalportfolio')
    internalstorage = fields.Char(string='internalstorage')
    financiallysettled = fields.Char(string='financiallysettled')
    planningquantity = fields.Float(string='planningquantity')
    shippingquantity = fields.Float(string='shippingquantity')
    planninguom = fields.Char(string='planninguom')
    shippinguom = fields.Char(string='shippinguom')
    zerooutqty = fields.Float(string='zerooutqty')
    implicitcost = fields.Char(string='implicitcost')
    financingbank = fields.Char(string='financingbank')
    financereference = fields.Char(string='financereference')
    legtype = fields.Char(string='legtype')
    efp = fields.Char(string='efp')
    efpphysical = fields.Integer(string='efpphysical')
    efptriggerlot = fields.Integer(string='efptriggerlot')
    voyagesegment = fields.Char(string='voyagesegment')
    nominationstatus = fields.Char(string='nominationstatus')
    parkandloan = fields.Char(string='parkandloan')
    financialmatchnumber = fields.Integer(string='financialmatchnumber')
    nativetradeprice = fields.Float(string='nativetradeprice')
    nativetradepricecurrency = fields.Char(string='nativetradepricecurrency')
    nativetradepriceuom = fields.Char(string='nativetradepriceuom')
    processingnumber = fields.Integer(string='processingnumber')
    invoicedate = fields.Date(string='invoicedate')
    grade = fields.Char(string='grade')
    masterdealid = fields.Integer(string='masterdealid')
    tradesubstatus = fields.Char(string='tradesubstatus')
    qpfinal = fields.Char(string='qpfinal')
    deliveryreference2 = fields.Char(string='deliveryreference2')
    deliveryreference3 = fields.Char(string='deliveryreference3')
    deliveryreference4 = fields.Char(string='deliveryreference4')
    deliveryreference5 = fields.Char(string='deliveryreference5')
    nominationkey = fields.Integer(string='nominationkey')
    extendedamtsysbaseccy = fields.Float(string='extendedamtsysbaseccy')
    extamtbasecurrency = fields.Float(string='extamtbasecurrency')
    icbasecurrency = fields.Char(string='icbasecurrency')
    extamtrptcurrency = fields.Float(string='extamtrptcurrency')
    icrptcurrency = fields.Char(string='icrptcurrency')
    stltosystembasefxrate = fields.Float(string='stltosystembasefxrate')
    stltoicbasefxrate = fields.Float(string='stltoicbasefxrate')
    stltoicrptfxrate = fields.Float(string='stltoicrptfxrate')
    eventdate = fields.Date(string='eventdate')
    billingaddress = fields.Char(string='billingaddress')
    mailingaddress = fields.Char(string='mailingaddress')
    shippingaddress = fields.Char(string='shippingaddress')
    masterdealrefnumber = fields.Char(string='masterdealrefnumber')
    marketsnapshot = fields.Char(string='marketsnapshot')
    internalbusinessunit = fields.Char(string='internalbusinessunit')
    intpaymentinstruction = fields.Char(string='intpaymentinstruction')
    companysector = fields.Char(string='companysector')
    pledgedtobank = fields.Char(string='pledgedtobank')
    contractsize = fields.Char(string='contractsize')
    accountingperiod = fields.Char(string='accountingperiod')
    productionperiod = fields.Char(string='productionperiod')
    taxnumber = fields.Char(string='taxnumber')
    erptaxcode = fields.Char(string='erptaxcode')
    surchargediscount = fields.Integer(string='surchargediscount')
    taxeffectivefromdate = fields.Date(string='taxeffectivefromdate')
    taxeffectivetodate = fields.Date(string='taxeffectivetodate')
    cptylevelinstrument = fields.Char(string='cptylevelinstrument')
    ticketnumber = fields.Integer(string='ticketnumber')
    ticketreference1 = fields.Char(string='ticketreference1')
    ticketreference2 = fields.Char(string='ticketreference2')
    ticketreference3 = fields.Char(string='ticketreference3')
    isfullyticketed = fields.Char(string='isfullyticketed')
    drivername = fields.Char(string='drivername')
    driverid = fields.Char(string='driverid')
    folioaccount = fields.Char(string='folioaccount')
    folioaccountnumber = fields.Char(string='folioaccountnumber')
    transporter = fields.Integer(string='transporter')
    registrationno = fields.Char(string='registrationno')
    blnumber = fields.Char(string='blnumber')
    tradeinputdate = fields.Date(string='tradeinputdate')
    triggerexpiry = fields.Date(string='triggerexpiry')
    imported = fields.Char(string='imported')
    alternatepayer = fields.Char(string='alternatepayer')
    sectiontype = fields.Char(string='sectiontype')
    transfercompletiondate = fields.Date(string='transfercompletiondate')
    parentinvoice = fields.Integer(string='parentinvoice')
    matchnumber = fields.Integer(string='matchnumber')
    reachcategory = fields.Char(string='reachcategory')
    bondednonbonded = fields.Char(string='bondednonbonded')
    tradelastmodifieddate = fields.Date(string='tradelastmodifieddate')
    transfercreatedby = fields.Char(string='transfercreatedby')
    commoditygroup1 = fields.Char(string='commoditygroup1')
    commoditygroup2 = fields.Char(string='commoditygroup2')
    costexternalcategory = fields.Integer(string='costexternalcategory')
    costinternalcategory = fields.Integer(string='costinternalcategory')
    exchcontracttype = fields.Char(string='exchcontracttype')
    passthroughcost = fields.Char(string='passthroughcost')
    deliveryperiod = fields.Date(string='deliveryperiod')
    certeffectivedate = fields.Date(string='certeffectivedate')
    certexpirydate = fields.Date(string='certexpirydate')
    mottype = fields.Char(string='mottype')
    actualextendedamount = fields.Float(string='actualextendedamount')
    cleared = fields.Char(string='cleared')
    custominvoicenumber = fields.Char(string='custominvoicenumber')
    deliverystartdate = fields.Date(string='deliverystartdate')
    deliveryenddate = fields.Date(string='deliveryenddate')
    estimatedextendedamount = fields.Float(string='estimatedextendedamount')
    stptrade = fields.Char(string='stptrade')
    intercompany = fields.Char(string='intercompany')
    internal = fields.Char(string='internal')
    license = fields.Char(string='license')
    locationbsoption = fields.Char(string='locationbsoption')
    mtmpricingtype = fields.Char(string='mtmpricingtype')
    nomtranstype = fields.Char(string='nomtranstype')
    packaging = fields.Char(string='packaging')
    parentlocation = fields.Char(string='parentlocation')
    passthrough = fields.Char(string='passthrough')
    paymentterm = fields.Char(string='paymentterm')
    repotype = fields.Char(string='repotype')
    settlementccy = fields.Char(string='settlementccy')
    settlementuom = fields.Char(string='settlementuom')
    specification = fields.Char(string='specification')
    tolerancetypeenum = fields.Integer(string='tolerancetypeenum')
    tradepriceon = fields.Char(string='tradepriceon')
    companyagreementtypename = fields.Char(string='companyagreementtypename')
    contactperson = fields.Char(string='contactperson')
    calculateddemurrage = fields.Float(string='calculateddemurrage')
    freightdelivery = fields.Integer(string='freightdelivery')
    initialclaim = fields.Float(string='initialclaim')
    lot = fields.Float(string='lot')
    strategyl1 = fields.Char(string='strategyl1')
    strategyl2 = fields.Char(string='strategyl2')
    strategyl3 = fields.Char(string='strategyl3')
    strategyl4 = fields.Char(string='strategyl4')
    strategyl5 = fields.Char(string='strategyl5')
    totaldemurragehours = fields.Char(string='totaldemurragehours')
    vehicle = fields.Char(string='vehicle')
    costcenter = fields.Char(string='costcenter')
    companycode = fields.Char(string='companycode')
    glcontracttype = fields.Char(string='glcontracttype')
    icparent = fields.Char(string='icparent')
    lotsize = fields.Float(string='lotsize')
    matchtype = fields.Char(string='matchtype')
    priorinvoicenumber = fields.Integer(string='priorinvoicenumber')
    profitcenter = fields.Char(string='profitcenter')
    tccontractnumber = fields.Integer(string='tccontractnumber')
    costallocation = fields.Char(string='costallocation')
    futuretradetype = fields.Char(string='futuretradetype')
    portfolio = fields.Char(string='portfolio')
    taxcode = fields.Char(string='taxcode')
    parentcashflowid = fields.Integer(string='parentcashflowid')
    hazardous = fields.Char(string='hazardous')
    coacheck = fields.Char(string='coacheck')
    animalfeed = fields.Char(string='animalfeed')
    reach = fields.Char(string='reach')
    reachregistrationno = fields.Char(string='reachregistrationno')
    unnumber = fields.Char(string='unnumber')
    unpackaging = fields.Char(string='unpackaging')
    shelflifeinyears = fields.Float(string='shelflifeinyears')
    customer = fields.Char(string='customer')
    serviceprovider = fields.Char(string='serviceprovider')
    producermanufacturing = fields.Char(string='producermanufacturing')
    repackertollerer = fields.Char(string='repackertollerer')
    vendor = fields.Char(string='vendor')
    other = fields.Char(string='other')
    hscodetype = fields.Char(string='hscodetype')
    hscodegeneral6 = fields.Char(string='hscodegeneral6')
    hscodelocal4 = fields.Char(string='hscodelocal4')
    hscodetotal10 = fields.Char(string='hscodetotal10')
    taxjurisdiction = fields.Char(string='taxjurisdiction')
    fromjurisdiction = fields.Char(string='fromjurisdiction')
    tojurisdiction = fields.Char(string='tojurisdiction')
    ticketreference4 = fields.Char(string='ticketreference4')
    ticketreference5 = fields.Char(string='ticketreference5')
    productionperioddate = fields.Date(string='productionperioddate')
    linkgroupname = fields.Char(string='linkgroupname')
    brokeraccount = fields.Char(string='brokeraccount')
    eventdatecolumn1 = fields.Date(string='eventdatecolumn1')
    eventdatecolumn2 = fields.Date(string='eventdatecolumn2')
    eventdatecolumn3 = fields.Date(string='eventdatecolumn3')
    eventdatecolumn4 = fields.Date(string='eventdatecolumn4')
    eventdatecolumn5 = fields.Date(string='eventdatecolumn5')
    eventdatecolumn6 = fields.Date(string='eventdatecolumn6')
    eventdatecolumn7 = fields.Date(string='eventdatecolumn7')
    eventdatecolumn8 = fields.Date(string='eventdatecolumn8')
    eventdatecolumn9 = fields.Date(string='eventdatecolumn9')
    eventdatecolumn10 = fields.Date(string='eventdatecolumn10')
    cropyear = fields.Char(string='cropyear')
    varietycode = fields.Char(string='varietycode')
    billoflading = fields.Date(string='billoflading')
    titletransferlocation = fields.Char(string='titletransferlocation')
    linespace = fields.Char(string='linespace')
    mtvolume = fields.Float(string='mtvolume')
    stockinoutid = fields.Integer(string='stockinoutid')
    carinitials = fields.Char(string='carinitials')
    carnumber = fields.Char(string='carnumber')
    bolnumber = fields.Char(string='bolnumber')
    storagetype = fields.Integer(string='storagetype')
    dealclassification = fields.Char(string='dealclassification')
    description = fields.Char(string='description')
    forcemajeure = fields.Char(string='forcemajeure')
    overridecostrevenue = fields.Char(string='overridecostrevenue')
    pipeline = fields.Char(string='pipeline')
    period = fields.Char(string='period')
    periodtype = fields.Char(string='periodtype')
    debitaccount = fields.Char(string='debitaccount')
    creditaccount = fields.Char(string='creditaccount')
    isgladjustment = fields.Char(string='isgladjustment')
    netvolume = fields.Float(string='netvolume')
    grossvolume = fields.Float(string='grossvolume')
    productcode = fields.Char(string='productcode')
    productsymbol = fields.Char(string='productsymbol')
    lotequivalent = fields.Float(string='lotequivalent')
    brokeraccounttype = fields.Char(string='brokeraccounttype')
    financingbankaccount = fields.Char(string='financingbankaccount')
    customsectionnumber = fields.Char(string='customsectionnumber')
    customtradenumber = fields.Char(string='customtradenumber')
    erpcustomerid = fields.Char(string='erpcustomerid')
    erpvendorid = fields.Char(string='erpvendorid')
    deliveryorigin = fields.Char(string='deliveryorigin')
    carriagename = fields.Char(string='carriagename')
    transportcarriagetype = fields.Char(string='transportcarriagetype')
    lastmodifydate = fields.Char(string='lastmodifydate')
    birecordcreationdate = fields.Date(string='birecordcreationdate')
    
    def import_cashflow(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
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
                self.create_update_cashflow('cashflow', json_data)
                interface.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_cashflow(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('cashflow')
        max_synced_date = self.env['cashflow.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                         order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
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
                self.regular_update_cashflow('cashflow', json_data)
                interface.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
            
    def force_sync_cashflow(self,date):
        interface = self.env['fusion.sync.history']
        last_sync = date
        # max_synced_date = self.env['cashflow.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
        #                                                                  order='lastmodifydate desc')
        # if max_synced_date:
        #     last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
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
                self.regular_update_cashflow('cashflow', json_data)
                interface.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    def sync_missing_cashflows(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2022-01-01'
        max_synced_date = self.env['cashflow.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                        order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
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
                self.sync_missing_cashflow('cashflow', json_data)
                interface.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_cashflow(self, interface_type, json_data):
        all = self.env['cashflow.controller.bi'].search([])
        for data in json_data:
            exists = all.search([('cashflowid', '=', data['cashflowid'])])
            if exists:
                continue
            else:
                self.env['cashflow.controller.bi'].create(data)
                self.env.cr.commit()
    
    def regular_update_cashflow(self, interface_type, json_data):
        # if interface_type == 'cashflow':
        #     existing_ids = set(self.env['cashflow.controller.bi'].search([]).mapped('cashflowid'))
        #     new_entries = [data for data in json_data if data['cashflowid'] not in existing_ids]
        #     # Process each item in json_data
        #     for data in new_entries:
        #         self.env['cashflow.controller.bi'].create(data)
        #         self.env.cr.commit()
        all_cfs = self.env['cashflow.controller.bi'].search([])
        for data in json_data:
            exists = all_cfs.search([('cashflowid', '=', data['cashflowid'])])
            if exists:
                all_cfs.search([('cashflowid', '=', data['cashflowid'])]).unlink()
                self.env['cashflow.controller.bi'].create(data)
            else:
                self.env['cashflow.controller.bi'].create(data)
                # self.env.cr.commit()
    
    def sync_missing_cashflow(self, interface_type, json_data):
        if interface_type == 'cashflow':
            all_cfs = self.env['cashflow.controller.bi'].search([])
            for data in json_data:
                exists = all_cfs.search([('cashflowid', '=', data['cashflowid'])])
                if exists:
                    self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
                    self.env['cashflow.controller.bi'].create(data)
                else:
                    self.env['cashflow.controller.bi'].create(data)
                    
    # def re_fetch(self):
    #     all_cfs = self.env['cashflow.controller.bi'].search([])
    #     for rec in self:
    #         exists = all_cfs.search([('cashflowid', '=', rec.cashflowid)])
    #         if exists:
    #             self.env['cashflow.controller.bi'].search(
    #                 [('cashflowid', '=', rec.cashflowid)]).unlink()
    #             self.env['cashflow.controller.bi'].create(data)
    #         else:
    #             self.env['cashflow.controller.bi'].create(data)
    #
            
               
                    # self.env.cr.commit()
        