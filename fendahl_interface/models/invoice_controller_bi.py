from odoo import models, fields
import requests
import logging
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)


class InvoiceControllerBI(models.Model):
    _name = 'invoice.controller.bi'
    _description = 'Invoice Controller Business Intelligence'
    
    invoicenumber = fields.Integer(string="InvoiceNumber")
    provisionalenum = fields.Char(string="ProvisionalEnum")
    invoicedate = fields.Char(string="InvoiceDate")
    paymentduedate = fields.Char(string="PaymentDueDate")
    counterparty = fields.Char(string="Counterparty")
    internalcompany = fields.Char(string="InternalCompany")
    commodity = fields.Char(string="Commodity")
    location = fields.Char(string="Location")
    invoiceamt = fields.Char(string="InvoiceAmt")
    paidamt = fields.Char(string="PaidAmt")
    openamt = fields.Char(string="OpenAmt")
    paidreceived = fields.Char(string="PaidReceived")
    amtcurrency = fields.Char(string="AmtCurrency")
    ourinvoiceref = fields.Char(string="OurInvoiceRef")
    theirinvoiceref = fields.Char(string="TheirInvoiceRef")
    invoicestatus = fields.Char(string="InvoiceStatus")
    fullypaiddate = fields.Char(string="FullyPaidDate")
    lastpaymentdate = fields.Char(string="LastPaymentDate")
    refcurrency = fields.Char(string="RefCurrency")
    currencyindexentry = fields.Char(string="CurrencyIndexEntry")
    venture = fields.Char(string="Venture")
    actperiodcode = fields.Char(string="ActPeriodCode")
    paymentmethod = fields.Char(string="PaymentMethod")
    transmitstatus = fields.Char(string="TransmitStatus")
    paymentid = fields.Char(string="PaymentId")
    displayinvoiceid = fields.Char(string="DisplayInvoiceId")
    ourpaymentinstr = fields.Char(string="OurPaymentInstr")
    theirpaymentinstr = fields.Char(string="TheirPaymentInstr")
    paymentreleasedate = fields.Char(string="PaymentReleaseDate")
    payablereceivable = fields.Char(string="PayableReceivable")
    postingdate = fields.Char(string="PostingDate")
    strategycode = fields.Char(string="StrategyCode")
    originlocation = fields.Char(string="OriginLocation")
    gradecategory = fields.Char(string="GradeCategory")
    mot = fields.Char(string="Mot")
    sapactperiod = fields.Char(string="SapActPeriod")
    sappostingdate = fields.Char(string="SapPostingDate")
    currentaccountingperiod = fields.Char(string="CurrentAccountingPeriod")
    billtoparty = fields.Char(string="BillToParty")
    payer = fields.Char(string="Payer")
    shiptoparty = fields.Char(string="ShipToParty")
    invoicepresentedby = fields.Char(string="InvoicePresentedBy")
    invoicecreatedby = fields.Char(string="InvoiceCreatedBy")
    blockedforpayment = fields.Char(string="BlockedForPayment")
    adjustedduedate = fields.Char(string="AdjustedDueDate")
    isfinanciallysettled = fields.Char(string="IsFinanciallySettled")
    approver1 = fields.Char(string="Approver1")
    approver2 = fields.Char(string="Approver2")
    invoiceopenstatus = fields.Char(string="InvoiceOpenStatus")
    displayinvoice = fields.Char(string="DisplayInvoice")
    accountingperioddate = fields.Char(string="AccountingPeriodDate")
    postingstatusenum = fields.Char(string="PostingStatusEnum")
    postingneededstatusenum = fields.Char(string="PostingNeededStatusEnum")
    batchprocessid = fields.Char(string="BatchProcessId")
    basecurrency = fields.Char(string="BaseCurrency")
    reportingcurrency = fields.Char(string="ReportingCurrency")
    invoiceamtbasecurrency = fields.Char(string="InvoiceAmtBaseCurrency")
    invoiceamtreportingcurrency = fields.Char(string="InvoiceAmtReportingCurrency")
    externalreferencenumber = fields.Char(string="ExternalReferenceNumber")
    masterdealid = fields.Char(string="MasterDealId")
    referencenumber = fields.Char(string="ReferenceNumber")
    ispledgedtobank = fields.Boolean(string="IsPledgedToBank")
    productdescription = fields.Char(string="ProductDescription")
    paymentstatus = fields.Char(string="PaymentStatus")
    counterpartylevelinstrument = fields.Char(string="CounterpartyLevelInstrument")
    invoicetype = fields.Char(string="InvoiceType")
    fxrate = fields.Char(string="FxRate")
    navpostingdate = fields.Char(string="NavPostingDate")
    invoicecreationdate = fields.Char(string="InvoiceCreationDate")
    taxclausedetailcode = fields.Char(string="TaxClauseDetailCode")
    taxclausedescription = fields.Char(string="TaxClauseDescription")
    postinggroup = fields.Char(string="PostingGroup")
    allocatedamount = fields.Char(string="AllocatedAmount")
    openallocation = fields.Char(string="OpenAllocation")
    businessunit = fields.Char(string="BusinessUnit")
    overrideextendedamount = fields.Char(string="OverrideExtendedAmount")
    isoverrideextendedamount = fields.Char(string="IsOverrideExtendedAmount")
    counterpartname = fields.Char(string="CounterpartName")
    issegmentfinal = fields.Char(string="IsSegmentFinal")
    parentinvoiceid = fields.Char(string="ParentInvoiceId")
    countryoforigin = fields.Char(string="CountryOfOrigin")
    countryofload = fields.Char(string="CountryOfLoad")
    countryofdischarge = fields.Char(string="CountryOfDischarge")
    isanimalfeed = fields.Boolean(string="IsAnimalFeed")
    reachcategory = fields.Char(string="ReachCategory")
    cropyear = fields.Char(string="CropYear")
    variety = fields.Char(string="Variety")
    titletransferlocation = fields.Char(string="TitleTransferLocation")
    netting = fields.Char(string="Netting")
    vehiclemottype = fields.Char(string="VehicleMotType")
    intapprovedperson = fields.Char(string="IntApprovedPerson")
    extapprovedperson = fields.Char(string="ExtApprovedPerson")
    navpackageid = fields.Char(string="NavPackageId")
    navinvoiceid = fields.Char(string="NavInvoiceId")
    packagingcode = fields.Char(string="PackagingCode")
    licensecode = fields.Char(string="LicenseCode")
    specificationcode = fields.Char(string="SpecificationCode")
    mirrorinvoicemasterid = fields.Char(string="MirrorInvoiceMasterId")
    transfercommencementdate = fields.Char(string="TransferCommencementDate")
    invoiceraisedon = fields.Char(string="InvoiceRaisedOn")
    isallocatetolc = fields.Boolean(string="IsAllocateToLc")
    weightfinalat = fields.Char(string="WeightFinalAt")
    custominvoicenumber = fields.Char(string="CustomInvoiceNumber")
    cpdate = fields.Char(string="CpDate")
    vessel = fields.Char(string="Vessel")
    material = fields.Char(string="Material")
    accountpaymentstatust = fields.Char(string="AccountPaymentStatust")
    invoicecategory = fields.Char(string="InvoiceCategory")
    isattachmentavailable = fields.Char(string="IsAttachmentAvailable")
    isnotesavailable = fields.Char(string="IsNotesAvailable")
    book = fields.Char(string="Book")
    positionstatus = fields.Char(string="PositionStatus")
    writeoffamt = fields.Char(string="WriteOffAmt")
    customtradenumber = fields.Char(string="CustomTradeNumber")
    customsectionnumber = fields.Char(string="CustomSectionNumber")
    quantity = fields.Char(string="Quantity")
    erppostingdate = fields.Char(string="ErpPostingDate")
    erpaccountingperiod = fields.Char(string="ErpAccountingPeriod")
    invoiceqtyuom = fields.Char(string="InvoiceQtyUom")
    ispaymentdueoverridden = fields.Char(string="IsPaymentDueOverridden")
    invoicelinkid = fields.Char(string="InvoiceLinkId")
    refinvoiceid = fields.Char(string="RefInvoiceId")
    refcustominvoiceid = fields.Char(string="RefCustomInvoiceId")
    letterofcredit = fields.Char(string="LetterOfCredit")
    certificateno = fields.Char(string="CertificateNo")
    taxcurrency = fields.Char(string="TaxCurrency")
    invoiceamttaxccyexcl = fields.Char(string="InvoiceAmtTaxCcyExcl")
    invoiceamttaxccyincl = fields.Char(string="InvoiceAmtTaxCcyIncl")
    taxamttaxccy = fields.Char(string="TaxAmtTaxCcy")
    samplerequired = fields.Char(string="SampleRequired")
    samplingprocess = fields.Char(string="SamplingProcess")
    ourvatnumber = fields.Char(string="OurVatNumber")
    theirvatnumber = fields.Char(string="TheirVatNumber")
    companycategory = fields.Char(string="CompanyCategory")
    arbitrationcode = fields.Char(string="ArbitrationCode")
    periodtype = fields.Char(string="PeriodType")
    docclassification = fields.Char(string="DocClassification")
    writeoffamount = fields.Char(string="WriteOffAmount")
    writeoffamountcurrency = fields.Char(string="WriteOffAmountCurrency")
    invoicevaluedate = fields.Char(string="InvoiceValueDate")
    isgeneratecost = fields.Char(string="IsGenerateCost")
    origin = fields.Char(string="Origin")
    portfolio = fields.Char(string="Portfolio")
    grade = fields.Char(string="Grade")
    invoiceamountexcltax = fields.Char(string="InvoiceAmountExclTax")
    invoiceamountinctax = fields.Char(string="InvoiceAmountIncTax")
    taxamount = fields.Char(string="TaxAmount")
    operator = fields.Char(string="Operator")
    writeoffdate = fields.Char(string="WriteOffDate")
    invoicereference = fields.Char(string="InvoiceReference")
    isadjusted = fields.Boolean(string="IsAdjusted")
    transportcarriage = fields.Char(string="TransportCarriage")
    transportcarriagecode = fields.Char(string="TransportCarriageCode")
    ismigrated = fields.Char(string="IsMigrated")
    paymentcurrency = fields.Char(string="PaymentCurrency")
    tradelinkcode = fields.Char(string="TradeLinkCode")
    tradelinkid = fields.Char(string="TradeLinkId")
    lockid = fields.Integer(string="LockId")
    statusenum = fields.Char(string="StatusEnum")
    modifypersonid = fields.Char(string="ModifyPersonId")
    modifyperson = fields.Char(string="ModifyPerson")
    lastmodifydate = fields.Char(string="LastModifyDate")
    customerid = fields.Char(string="CustomerId")
    birecordcreationdate = fields.Char(string="BiRecordCreationDate")
    
    def import_invoice(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/invoice"
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
                self.create_update_invoice('invoice', json_data)
                interface.update_sync_interface('invoice')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def process_odoo_transaction_action(self):
        interface = self.env['fusion.sync.history']
        last_processing_date = interface.get_last_processing('invoice')
        trades_to_process = self.env['invoice.controller.bi'].search([('lastmodifydate', '>=', last_processing_date)])
        for rec in trades_to_process:
            if rec.internalcompany == 'KEMEXON LTD':
                rec.create_bill(False)
        interface.update_processing_date('invoice')
    
    def sync_invoice(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('invoice')
        max_synced_date = self.env['invoice.controller.bi'].search_read([], fields=['lastmodifydate'], limit=1,
                                                                        order='lastmodifydate desc')
        if max_synced_date:
            last_sync = max_synced_date[0]['lastmodifydate']
        url = "https://fusionsqlmirrorapi.azure-api.net/api/invoice"
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
                self.regular_update_invoice('invoice', json_data)
                interface.update_sync_interface('invoice')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_invoice(self, interface_type, json_data):
        if interface_type == 'invoice':
            all = self.env['invoice.controller.bi'].search([])
            if all:
                for data in json_data:
                    exists = all.search([('invoicenumber', '=', data['invoicenumber'])])
                    if exists:
                        return
                    else:
                        self.env['invoice.controller.bi'].create(data)
                        self.env.cr.commit()
            else:
                for data in json_data:
                    self.env['invoice.controller.bi'].create(data)
                    self.env.cr.commit()
    
    def regular_update_invoice(self, interface_type, json_data):
        if interface_type == 'invoice':
            all = self.env['invoice.controller.bi'].search([])
            for data in json_data:
                exists = all.search([('invoicenumber', '=', data['invoicenumber'])])
                if exists:
                    self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])]).unlink()
                    self.env['invoice.controller.bi'].create(data)
                else:
                    self.env['invoice.controller.bi'].create(data)
                    self.env.cr.commit()
    
    def update_existing_invoice_header(self, existing_invoice, po, pol):
        existing_invoice.write({'purchase_id': po.id})
        existing_invoice.write({'invoice_origin': po.name})
    
    def update_existing_product_line(self, existing_line, cf, pol, tax_rate_record, multiplier):
        product = self.env['fusion.sync.history'].validate_product(cf.commodity, cf.material, cf.quantityuom)
        uom = self.env['fusion.sync.history'].validate_uom(cf.material, cf.quantityuom)
        existing_line.name = pol.product_id.name
        existing_line.product_id = product.id
        existing_line.product_uom_id = uom.id
        existing_line.quantity = float(cf.quantity)
        existing_line.price_unit = cf.price * multiplier
        existing_line.purchase_line_id = pol.id
        existing_line.analytic_distribution = pol.analytic_distribution
        existing_line.tax_ids = [
            (6, 0, [tax_rate_record.id])] if tax_rate_record else existing_line.tax_ids if existing_line.tax_ids else [
            (6, 0, [])]
    
    def create_product_line_existing_invoice(self, existing_invoice, cf, product, uom, pol, tax_rate_record, multiplier,
                                             company):
        self.env['account.move.line'].create({
            'move_id': existing_invoice.id,
            'name': pol.product_id.name,
            'product_id': product.id,
            'product_uom_id': uom.id,
            'quantity': float(cf.quantity),
            'price_unit': float(cf.price) * multiplier,
            'purchase_line_id': pol.id,
            'analytic_distribution': pol.analytic_distribution,
            'cashflow_id': cf.cashflowid,
            'tax_ids': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])]
        })
    
    def update_existing_other_invoice(self, existing_invoice, cf, po, pol, company):
        existing_invoice.button_draft()
        # link existing invoice
        self.update_existing_invoice_header(existing_invoice, po, pol)
        existing_line = self.env['account.move.line'].search([('cashflow_id', '=', cf.cashflowid)])
        tax_rate_record = self.get_tax_rate_record(cf, company)
        product = self.env['fusion.sync.history'].validate_product(cf.commodity,
                                                                   cf.material,
                                                                   cf.quantityuom)
        uom = self.env['fusion.sync.history'].validate_uom(product,
                                                           cf.quantityuom)
        multiplier = 1
        if not cf.payablereceivable == 'Payable':
            multiplier = -1
        if existing_line:
            self.update_other_line_existing_invoice(existing_line, cf, pol, tax_rate_record, multiplier)
        else:
            self.create_other_line_existing_invoice(existing_invoice, cf, product, uom, pol, tax_rate_record,
                                                    multiplier, company)
        existing_invoice.action_post()
    
    def create_other_line_existing_invoice(self, existing_invoice, cf, product, uom, pol, tax_rate_record, multiplier,
                                           company):
        if cf.costtype in (
                'Pre-payment', 'Pre-payment_Rev', 'Provisional Payment',
                'Provisional Payment_Rev'):
            cost = self.env['fusion.sync.history'].validate_cost(cf.costtype)
            self.env['account.move.line'].create({
                'move_id': existing_invoice.id,
                'name': pol.product_id.name,
                'product_id': 312,
                'quantity': 1,
                'price_unit': float(cf.price) * -1,
                # 'purchase_line_id': pol.id if cf.invoicenumber == rec.invoicenumber else None,
                'analytic_distribution': pol.analytic_distribution,
                'cashflow_id': cf.cashflowid,
                'tax_ids': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [
                    (6, 0, [])]
            })
        else:
            cost = self.env['fusion.sync.history'].validate_cost(cf.costtype)
            self.env['account.move.line'].create({
                'move_id': existing_invoice.id,
                'name': pol.product_id.name,
                'product_id': cost.id,
                'quantity': float(cf.quantity),
                'price_unit': float(cf.price) * -1,
                # 'purchase_line_id': pol.id if cf.invoicenumber == rec.invoicenumber else None,
                'analytic_distribution': pol.analytic_distribution,
                'cashflow_id': cf.cashflowid,
                'tax_ids': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [
                    (6, 0, [])]
            })
    
    def update_other_line_existing_invoice(self, existing_line, cf, pol, tax_rate_record, multiplier):
        if cf.costtype in ('Pre-payment', 'Pre-payment_Rev', 'Provisional Payment', 'Provisional Payment_Rev'):
            existing_line.product_id = 312,
            existing_line.product_uom_id = 1,
            existing_line.quantity = 1,
            existing_line.price_unit = float(cf.extendedamount) * -1
            existing_line.purchase_line_id = pol.id
            existing_line.analytic_distribution = pol.analytic_distribution
            existing_line.tax_ids = [(6, 0, [
                tax_rate_record.id])] if tax_rate_record else existing_line.tax_ids if existing_line.tax_ids else [
                (6, 0, [])]
        else:
            cost = self.env['fusion.sync.history'].validate_cost(cf.costtype)
            existing_line.name = pol.product_id.name
            existing_line.product_id = cost.id
            existing_line.quantity = float(cf.quantity)
            existing_line.price_unit = float(cf.price) * -1
            existing_line.purchase_line_id = pol.id
            existing_line.analytic_distribution = pol.analytic_distribution
            existing_line.tax_ids = [(6, 0, [
                tax_rate_record.id])] if tax_rate_record else existing_line.tax_ids if existing_line.tax_ids else [
                (6, 0, [])]
    
    def build_product_invoice_vals(self, pol, po, company, rec, partner):
        
        return {
            'company_id': company.id,
            'invoice_origin': po.name,
            'partner_id': partner.id,
            'invoice_line_ids': [],
            'currency_id': self.env['res.currency'].search([('name', '=', rec.amtcurrency)], limit=1).id,
            'purchase_id': po.id,
            'custom_section_number': pol.custom_section_number,
            'invoice_date': rec.invoicedate,
            'date': rec.invoicedate,
            'ref': rec.theirinvoiceref,
            'invoice_date_due': rec.paymentduedate,
            'fusion_reference': rec.invoicenumber,
            'fusion_invoice_ref': rec.custominvoicenumber,
        }
    
    def build_other_invoice_vals(self, po, rec, partner, cf):
        return {
            'company_id': self.env['res.company'].search(
                [('name', '=', cf.internalcompany)], limit=1).id,
            # 'fusion_invoice_ref': rec.invoicenumber, # Vendor bill
            'invoice_origin': po.name,
            'partner_id': partner.id,
            'invoice_line_ids': [],
            'currency_id': self.env['res.currency'].search(
                [('name', '=', rec.amtcurrency)], limit=1).id,
            # po.currency_id.id, # self.env['res.currency'].search([(rec.material)rec.amtcurrency,
            'purchase_id': po.id,
            'custom_section_number': cf.customsectionnumber,
            # Link back to the purchase order
            'invoice_date': rec.invoicedate,
            'date': cf.invoicedate,
            'ref': cf['sectionno'] + str(cf['cashflowid']),
            'invoice_date_due': rec.paymentduedate,
            'fusion_reference': cf.invoicenumber,
            'fusion_invoice_ref': cf.custominvoicenumber,
        }
    
    def check_existing_invoice(self, invoicenumber):
        existing_invoice = self.env['account.move'].search(
            [('fusion_reference', '=ilike', str(invoicenumber) + ',%')])
        if existing_invoice:
            return existing_invoice
        else:
            return False
    
    def create_product_line(self, header, pol, cf, company):
        product = self.env['fusion.sync.history'].validate_product(cf.commodity,
                                                                   cf.material,
                                                                   cf.quantityuom)
        uom = self.env['fusion.sync.history'].validate_uom(product,
                                                           cf.quantityuom)
        multiplier = 1
        tax_rate_record = self.get_tax_rate_record(cf, company)
        if not cf.payablereceivable == 'Payable':
            multiplier = -1
        tax_rate_record = self.get_tax_rate_record(cf, company)
        invoice_line_vals = {
            'name': pol.product_id.name,
            'product_id': product.id,
            'product_uom_id': uom.id,
            'quantity': float(cf.quantity),
            'price_unit': cf.price * multiplier,
            'purchase_line_id': pol.id if cf.invoicenumber == cf.invoicenumber else None,
            'analytic_distribution': pol.analytic_distribution,
            'cashflow_id': cf.cashflowid,
            'tax_ids': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [
                (6, 0, [])]
        }
        header['invoice_line_ids'].append((0, 0, invoice_line_vals))
    
    def create_other_line(self, header, pol, cfl, company):
        multiplier = 1
        tax_rate_record = self.get_tax_rate_record(cfl, company)
        if not cfl.payablereceivable == 'Payable':
            multiplier = -1
        if cfl.costtype in (
                'Pre-payment', 'Pre-payment_Rev', 'Provisional Payment',
                'Provisional Payment_Rev'):
            cost = self.env['fusion.sync.history'].validate_cost(cfl.costtype)
            invoice_line_vals = {
                'name': pol.product_id.name,
                'product_id': 312,
                'quantity': 1,
                'price_unit': float(cfl.price) * multiplier,
                # 'purchase_line_id': pol.id if cfl.invoicenumber == rec.invoicenumber else None,
                'analytic_distribution': pol.analytic_distribution,
                'cashflow_id': cfl.cashflowid,
                'tax_ids': [
                    (6, 0, [tax_rate_record.id])] if tax_rate_record else [
                    (6, 0, [])]
            }
        else:
            cost = self.env['fusion.sync.history'].validate_cost(cfl.costtype)
            invoice_line_vals = {
                'name': pol.product_id.name,
                'product_id': cost.id,
                'quantity': float(cfl.quantity),
                'price_unit': float(cfl.price) * multiplier,
                # 'purchase_line_id': pol.id if cfl.invoicenumber == rec.invoicenumber else None,
                'analytic_distribution': pol.analytic_distribution,
                'cashflow_id': cfl.cashflowid,
                'tax_ids': [
                    (6, 0, [tax_rate_record.id])] if tax_rate_record else [
                    (6, 0, [])]
            }
        
        header['invoice_line_ids'].append((0, 0, invoice_line_vals))
    
    def validate_partner(self, cf):
        partner = self.env['res.partner'].search([('name', '=', cf.counterpart)],
                                                 limit=1)
        if not partner:
            partner_info = self.env['fusion.sync.history'].get_partner_info(
                cf.counterpart)
            if partner_info:
                partner = self.env['res.partner'].search(
                    [('short_name', '=', partner_info['configCode'])])
        return partner
    
    def get_cashflow(self, invoice_number):
        return self.env['cashflow.controller.bi'].search(
            [('invoicenumber', '=', invoice_number)])
    
    def get_related_partner_segment_cashflows(self, fusion_segment_code, costtype, partner):
        if costtype == 'Primary Settlement':
            return self.env['cashflow.controller.bi'].search([('sectionno', '=', fusion_segment_code),
                                                              ('cashflowstatus', '!=', 'Defunct'),
                                                              ('quantitystatus', '=', 'Actual')
                                                                 , ('counterpart', '=', partner)
                                                                 , ('costtype', '=', costtype)
                                                              ])
        
        else:
            return self.env['cashflow.controller.bi'].search([('sectionno', '=', fusion_segment_code),
                                                              ('cashflowstatus', '!=', 'Defunct'),
                                                              ('quantitystatus', '=', 'Actual')
                                                                 , ('counterpart', '=', partner)
                                                                 , ('costtype', 'not in',
                                                                    ('Primary Settlement', 'VAT', 'Tax'))
                                                              ])
    
    def getinvoiceref(self, ref):
        exists = self.env['account.move'].search([('ref', '=', ref)])
        if exists:
            ref = self.getinvoiceref(ref + '.')
            return ref
        else:
            return ref
    
    def create_bill(self):
        for rec in self:
            if rec.invoicestatus == 'Active':
                if rec.invoiceopenstatus == 'Send To Accounting':
                    company = self.env['res.company'].search([('name', '=', rec.internalcompany)], limit=1)
                    
                    cashflow_lines_all = self.env['cashflow.controller.bi'].search(
                        [('invoicenumber', '=', rec.invoicenumber), ('cashflowstatus', '!=', 'Defunct')])
                    cashflowlineswithbuysellall = cashflow_lines_all.read_group(
                        domain=[('invoicenumber', '=', rec.invoicenumber),
                                ('cashflowstatus', '!=', 'Defunct'),
                                ('buysell', '!=', False)],
                        fields=['buysell', 'counterpart', 'tradenumber'],  # Fields to load
                        groupby=['buysell', 'counterpart', 'tradenumber'],
                        lazy=False  # Get results for each partner directly
                    )
                    buysell = ""
                    if cashflowlineswithbuysellall:
                        cashflowlineswithbuysell =  cashflowlineswithbuysellall[0]
                        if cashflowlineswithbuysell['buysell'] == 'Buy':
                            buysell = "Buy"
                        elif cashflowlineswithbuysell['buysell'] == 'Sell':
                            tradecounterpart = self.env['trade.controller.bi'].search(
                                [('dealmasterid', '=', cashflowlineswithbuysell['tradenumber'])])
                            tradecounterpart = tradecounterpart[0].counterpartcompany
                            if tradecounterpart == cashflowlineswithbuysell['counterpart']:
                                buysell = "Sell"
                            else:
                                buysell = "Buy"
                    
                    if buysell == "":
                        buysell = "Buy" if rec.payablereceivable == "Payable" else "Sell"
                    
                    if buysell == "Buy":
                        existing_invoice = self.check_existing_invoice(rec.invoicenumber)
                        
                        if existing_invoice:
                            previousstatus = existing_invoice.state
                            invoice_reconciled_lines = self.get_reconciled_lines(existing_invoice)
                            existing_invoice.button_draft()
                            # existing_invoice.write({'purchase_id': po.id}) if po else None
                            cashflow_lines_po = cashflow_lines_all.read_group(
                                domain=[('invoicenumber', '=', rec.invoicenumber), ('cashflowstatus', '!=', 'Defunct')],
                                fields=['sectionno'],  # Fields to load
                                groupby=['sectionno'],
                                lazy=False)
                            invoice_origins = ''
                            for clp in cashflow_lines_po:
                                if clp['sectionno']:
                                    pol = self.env['purchase.order.line'].search(
                                        [('fusion_segment_code', '=', clp['sectionno'])])
                                    if pol:
                                        if pol.order_id:
                                            if invoice_origins == '':
                                                invoice_origins = pol.order_id.name
                                            else:
                                                invoice_origins = invoice_origins + ', ' + pol.order_id.name
                            existing_invoice.write({'invoice_origin': invoice_origins}) if invoice_origins else None
                            if existing_invoice:
                                for invoice in existing_invoice:
                                    invoice.ref = self.getinvoiceref(rec.theirinvoiceref)
                                    if invoice.company_id.id in (1, 2):
                                        costtypes = cashflow_lines_all.read_group(
                                            domain=[('invoicenumber', '=', rec.invoicenumber),
                                                    ('cashflowstatus', '!=', 'Defunct')],
                                            fields=['costtype'],  # Fields to load
                                            groupby=['costtype'],
                                            lazy=False)
                                        costtype_list = [ct['costtype'] for ct in costtypes]
                                        invoice.posted_before = False
                                        invoice.sequence_number = 0
                                        if "Primary Settlement" in costtype_list:
                                            expected_journal = self.env['account.journal'].search(
                                                [('name', '=', 'Purchases'),
                                                 ('company_id', '=', invoice.company_id.id)]).id
                                            if invoice.journal_id != expected_journal:
                                                invoice.journal_id=expected_journal
                                        elif 'Pre-payment_Rev' in costtype_list or 'Provisional Payment_Rev' in costtype_list or 'Pre-payment' in costtype_list or 'Provisional Payment' in costtype_list:
                                             expected_journal =  self.env['account.journal'].search(
                                                [('name', '=', 'Provisional Purchases'),
                                                 ('company_id', '=', invoice.company_id.id)]).id
                                             if invoice.journal_id != expected_journal:
                                                 invoice.journal_id = expected_journal
                                        else:
                                            expected_journal = self.env['account.journal'].search(
                                            [('name', '=', 'Purchases'),
                                             ('company_id', '=', invoice.company_id.id)]).id
                                            if invoice.journal_id != expected_journal:
                                                invoice.journal_id = expected_journal
                                        
                            
                            self.env.cr.commit()
                            if existing_invoice.line_ids:
                                cashflow_lines = cashflow_lines_all.read_group(
                                    domain=[('invoicenumber', '=', rec.invoicenumber),
                                            ('cashflowstatus', '!=', 'Defunct')],
                                    fields=['payablereceivable', 'costtype', 'commodity', 'material', 'quantityuom',
                                            'quantity', 'price', 'extendedamount'],  # Fields to load
                                    groupby=['erptaxcode', 'costtype', 'price', 'quantityuom', 'payablereceivable',
                                             'commodity', 'material'],
                                    lazy=False  # Get results for each partner directly
                                )

                                
                                receivables = sum(r['extendedamount'] for r in cashflow_lines if
                                                  r['payablereceivable'] == 'Receivable')
                                payables = sum(r['extendedamount'] for r in cashflow_lines if
                                               r['payablereceivable'] == 'Payable') * -1
                                extended_multiplier = 1
                                if payables > receivables:
                                    existing_invoice.move_type = 'in_invoice'
                                    extended_multiplier = -1
                                else:
                                    existing_invoice.move_type = 'in_refund'
                                    extended_multiplier = +1
                                
                                # if payables == 0 and receivables > 0:
                                #     existing_invoice.move_type = 'in_refund'
                                # elif payables < receivables:
                                #     quantity_multiplier = -1
                                #     existing_invoice.move_type = 'in_refund'
                                # else:
                                #     existing_invoice.move_type = 'in_invoice'
                                #
                                if cashflow_lines:
                                    for cfline in cashflow_lines:
                                        product_linez = existing_invoice.line_ids.filtered(
                                            lambda r: r.display_type == 'product')
                                        for product_lines in product_linez:
                                            if ((cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                    product_lines.product_id.name == "Down payment" and cfline[
                                                'costtype'] in (
                                                            'Pre-payment_Rev', 'Provisional Payment_Rev', 'Pre-payment',
                                                            'Provisional Payment')) and (
                                                    float(round(cfline['price'], 2)) == round(
                                                product_lines.price_unit, 2))
                                                    and ((product_lines.balance < 0 and (
                                                            cfline['extendedamount'] * -1) < 0) or (
                                                                 product_lines.balance > 0 and (
                                                                 cfline['extendedamount'] * -1) > 0))):
                                                self.update_existing_line(product_lines, company, cfline
                                                                          ,extended_multiplier, cashflow_lines_all,
                                                                          rec.invoicenumber)
                                            elif ((cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                          product_lines.product_id.name == "Down payment" and cfline[
                                                      'costtype'] in (
                                                                  'Pre-payment_Rev', 'Provisional Payment_Rev',
                                                                  'Pre-payment',
                                                                  'Provisional Payment')) and cfline[
                                                      'costtype'] != 'Primary Settlement'
                                                  and float(round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.price_unit, 2) and ((product_lines.balance > 0 >
                                                                                           cfline['extendedamount']) or (
                                                                                                  product_lines.balance < 0 <
                                                                                                  cfline[
                                                                                                             'extendedamount']))):
                                                self.update_existing_line(product_lines, company, cfline,
                                                                             extended_multiplier, cashflow_lines_all, rec.invoicenumber)
                                            elif ((cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                          product_lines.product_id.name == "Down payment" and cfline[
                                                      'costtype'] in (
                                                                  'Pre-payment_Rev', 'Provisional Payment_Rev',
                                                                  'Pre-payment',
                                                                  'Provisional Payment'))
                                                  and (float(round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.balance, 2) * -1) or float(
                                                        round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.balance, 2)):
                                                self.update_existing_line(product_lines, company, cfline,
                                                                             extended_multiplier, cashflow_lines_all, rec.invoicenumber)
                                            elif cfline['costtype'] != "Primary Settlement" and (
                                                    cfline['quantity'] == product_lines.quantity or cfline[
                                                'quantity'] * -1 == product_lines.quantity) and (
                                                    round(cfline['price'], 2) == product_lines.price_unit or round(
                                                    cfline['price'], 2) * -1 == product_lines.price_unit):
                                                self.update_existing_line(product_lines, company, cfline,
                                                                             extended_multiplier, cashflow_lines_all, rec.invoicenumber)
                                            elif (cfline['costtype'] != "Primary Settlement"
                                                  and (product_lines.quantity == 1 or product_lines.quantity == -1)
                                                  and (round(cfline['extendedamount'], 2) == product_lines.price_unit
                                                       or round(cfline['extendedamount'], 2) * -1 == product_lines.price_unit)):
                                                self.update_existing_line(product_lines, company, cfline,
                                                                             extended_multiplier, cashflow_lines_all, rec.invoicenumber)
                                            
                                
                                
                                else:
                                    log_error = self.env['fusion.sync.history.errors'].log_error(
                                        'InvoiceControllerBI',
                                        rec.invoicenumber,
                                        'Cashflow lines not found in Odoo',
                                        rec.internalcompany)
                                    raise UserError('Cashflow lines not found in Odoo')
                            
                            
                            else:
                                log_error = self.env['fusion.sync.history.errors'].log_error(
                                    'InvoiceControllerBI',
                                    rec.invoicenumber,
                                    'Invoice has no lines in Odoo.',
                                    rec.internalcompany)
                                raise UserError('Invoice has no lines in Odoo')
                            
                            if previousstatus == 'posted':
                                existing_invoice.action_post()
                                if invoice_reconciled_lines:
                                    self.reconcile_entries(invoice_reconciled_lines, existing_invoice)
                        else:
                            log_error = self.env['fusion.sync.history.errors'].log_error(
                                'InvoiceControllerBI',
                                rec.invoicenumber,
                                'Invoice not yet sent to Odoo. Please update the status of invoice to be SEND TO ACCOUNTING',
                                rec.internalcompany)
                            raise UserError(
                                'Invoice not yet sent to Odoo. Please update the status of invoice to be SEND TO ACCOUNTING', )
                            
                            # raise UserError('Invoice doesnt exist in Odoo.')
                    
                    elif buysell == "Sell":
                        sol = self.env['sale.order.line'].search([('id', '=', 0)])
                        so = self.env['sale.order'].search([('id', '=', 0)])
                        
                        existing_invoice = self.check_existing_invoice(rec.invoicenumber)
                        if existing_invoice:
                            previousstatus = existing_invoice.state
                            invoice_reconciled_lines = self.get_reconciled_lines(existing_invoice)
                            existing_invoice.button_draft()
                            cashflow_lines_so = self.env['cashflow.controller.bi'].read_group(
                                domain=[('invoicenumber', '=', rec.invoicenumber), ('cashflowstatus', '!=', 'Defunct')],
                                fields=['sectionno'],  # Fields to load
                                groupby=['sectionno'],
                                lazy=False  # Get results for each partner directly
                            )
                            invoice_origins = ''
                            for clp in cashflow_lines_so:
                                if clp['sectionno']:
                                    sol = self.env['sale.order.line'].search(
                                        [('fusion_segment_code', '=', clp['sectionno'])])
                                    if invoice_origins == '':
                                        invoice_origins = sol.order_id.name
                                    else:
                                        invoice_origins = invoice_origins + ', ' + sol.order_id.name
                            
                            existing_invoice.write({'invoice_origin': invoice_origins}) if invoice_origins else None
                            if existing_invoice:
                                
                                for invoice in existing_invoice:
                                    
                                    invoice.deal_ref = self.getinvoiceref(rec.theirinvoiceref)
                                    if invoice.company_id.id in (1, 2):
                                        costtypes = cashflow_lines_all.read_group(
                                            domain=[('invoicenumber', '=', rec.invoicenumber),
                                                    ('cashflowstatus', '!=', 'Defunct')],
                                            fields=['costtype'],  # Fields to load
                                            groupby=['costtype'],
                                            lazy=False)
                                        costtype_list = [ct['costtype'] for ct in costtypes]
                                      
                                        if "Primary Settlement" in costtype_list:
                                            expected_journal = self.env['account.journal'].search(
                                                [('name', '=', 'Purchases'),
                                                 ('company_id', '=', invoice.company_id.id)])
                                            if invoice.journal_id != expected_journal:
                                                invoice.posted_before = False
                                                invoice.sequence_number = 0
                                                invoice.journal_id=expected_journal.id
                                        elif 'Pre-payment_Rev' in costtype_list or 'Provisional Payment_Rev' in costtype_list or 'Pre-payment' in costtype_list or 'Provisional Payment' in costtype_list:
                                            expected_journal = self.env['account.journal'].search(
                                                [('name', '=', 'Provisional Purchases'),
                                                 ('company_id', '=', invoice.company_id.id)])
                                            if invoice.journal_id != expected_journal:
                                                invoice.posted_before = False
                                                invoice.sequence_number = 0
                                                invoice.journal_id=expected_journal.id
                                        else:
                                            expected_journal  = self.env['account.journal'].search(
                                                [('name', '=', 'Purchases'),
                                                 ('company_id', '=', invoice.company_id.id)])
                                            if invoice.journal_id != expected_journal:
                                                invoice.posted_before = False
                                                invoice.sequence_number = 0
                                                invoice.journal_id=expected_journal.id
                                
                            
                            # existing_invoice.write({'sale_line_id': so.id}) if so else None
                            existing_invoice.write({'invoice_origin': so.name}) if so else None
                            if existing_invoice.line_ids:
                                # cashflow_line = self.env['cashflow.controller.bi'].search(
                                #     [('invoicenumber', '=', rec.invoicenumber)])
                                cashflow_lines = self.env['cashflow.controller.bi'].read_group(
                                    domain=[('invoicenumber', '=', rec.invoicenumber),
                                            ('cashflowstatus', '!=', 'Defunct'),
                                            ('buysell', '=', 'Sell')],
                                    fields=['payablereceivable', 'costtype', 'commodity',
                                            'material', 'quantityuom', 'quantity', 'price', 'extendedamount'],
                                    # Fields to load
                                    groupby=['erptaxcode', 'costtype', 'price', 'quantityuom', 'payablereceivable',
                                             'commodity', 'material'],
                                    lazy=False  # Get results for each partner directly
                                )
                                # if existing_invoice.move_type=='out_refund':
                                receivables = sum(r['extendedamount'] for r in cashflow_lines if
                                                  r['payablereceivable'] == 'Receivable')
                                payables = sum(r['extendedamount'] for r in cashflow_lines if
                                               r['payablereceivable'] == 'Payable') * -1
                                
                                extended_multiplier = 1
                                if receivables > payables :
                                    existing_invoice.move_type = 'out_invoice'
                                    extended_multiplier = 1
                                else:
                                    existing_invoice.move_type = 'out_refund'
                                    extended_multiplier = -1

                                if cashflow_lines:
                                    for cfline in cashflow_lines:
                                        product_linez = existing_invoice.line_ids.filtered(
                                            lambda r: r.display_type == 'product')
                                        for product_lines in product_linez:
                                            if (cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                    product_lines.product_id.name == "Down payment" and cfline[
                                                'costtype'] in (
                                                            'Pre-payment_Rev', 'Provisional Payment_Rev', 'Pre-payment',
                                                            'Provisional Payment')) and (
                                                    float(round(cfline['price'], 2)) == round(product_lines.price_unit,
                                                                                              2)) and (
                                                    (product_lines.balance > 0 and cfline['extendedamount'] < 0) or (
                                                    product_lines.balance < 0 and cfline['extendedamount'] > 0)):
                                                self.update_existing_si_line(product_lines, company, cfline,
                                                                             extended_multiplier, rec.invoicenumber)
                                            elif ((cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                          product_lines.product_id.name == "Down payment" and cfline[
                                                      'costtype'] in (
                                                                  'Pre-payment_Rev', 'Provisional Payment_Rev',
                                                                  'Pre-payment',
                                                                  'Provisional Payment')) and cfline[
                                                      'costtype'] != 'Primary Settlement'
                                                  and float(round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.price_unit, 2) and ((product_lines.balance > 0 and
                                                                                           cfline[
                                                                                               'extendedamount'] < 0) or (
                                                                                                  product_lines.balance < 0 and
                                                                                                  cfline[
                                                                                                      'extendedamount'] > 0))):
                                                self.update_existing_si_line(product_lines, company, cfline,
                                                                             extended_multiplier, rec.invoicenumber)
                                            elif ((cfline['costtype'] == 'Primary Settlement' and cfline[
                                                'material'] == product_lines.product_id.name) or (
                                                          product_lines.product_id.name == "Down payment" and cfline[
                                                      'costtype'] in (
                                                                  'Pre-payment_Rev', 'Provisional Payment_Rev',
                                                                  'Pre-payment',
                                                                  'Provisional Payment'))
                                                  and (float(round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.balance, 2) * -1) or float(
                                                        round(cfline['extendedamount'], 2)) == round(
                                                        product_lines.balance, 2)):
                                                self.update_existing_si_line(product_lines, company, cfline,
                                                                             extended_multiplier, rec.invoicenumber)
                                            elif cfline['costtype'] != "Primary Settlement" and (cfline['quantity'] == product_lines.quantity or cfline['quantity']*-1 == product_lines.quantity) and (round(cfline['price'],2)== product_lines.price_unit or round(cfline['price'],2) *-1== product_lines.price_unit):
                                                    self.update_existing_si_line(product_lines, company, cfline,
                                                                                 extended_multiplier, rec.invoicenumber)
                                            elif (cfline['costtype'] != "Primary Settlement"
                                                  and (product_lines.quantity == 1 or product_lines.quantity == -1)
                                                  and (round(cfline['extendedamount'], 2) == product_lines.price_unit
                                                       or round(cfline['extendedamount'], 2) * -1 == product_lines.price_unit)):
                                                self.update_existing_si_line(product_lines, company, cfline,
                                                                             extended_multiplier, rec.invoicenumber)
                                else:
                                    log_error = self.env['fusion.sync.history.errors'].log_error(
                                        'InvoiceControllerBI',
                                        rec.invoicenumber,
                                        'Cashflow Lines not found in Odoo',
                                        rec.internalcompany)
                                    raise UserError(
                                        'Cashflow Lines not found in Odoo')
                                self.env.cr.commit()
                                if previousstatus == 'posted':
                                    existing_invoice.action_post()
                                    if invoice_reconciled_lines:
                                        self.reconcile_entries(invoice_reconciled_lines, existing_invoice)
                            else:
                                log_error = self.env['fusion.sync.history.errors'].log_error(
                                    'InvoiceControllerBI',
                                    rec.invoicenumber,
                                    'Invoice Lines not found in Odoo',
                                    rec.internalcompany)
                                raise UserError('Invoice Lines not found in Odoo')
                        else:
                            log_error = self.env['fusion.sync.history.errors'].log_error(
                                'InvoiceControllerBI',
                                rec.invoicenumber,
                                'Invoice is not yet synced to Odoo',
                                rec.internalcompany)
                            raise UserError('Invoice is not yet synced to Odoo')
            elif rec.invoicestatus != 'Active':
                existing_invoice = self.check_existing_invoice(rec.invoicenumber)
                if existing_invoice:
                    existing_invoice.button_draft()
                    existing_invoice.button_cancel()
    
    def reconcile_entries(self, invoice_reconciled_lines, existing_invoice):
        reconcile_obj = self.pool.get('account.partial.reconcile')
        # invoice_reconciled_line = existing_invoice.line_ids.filtered(lambda p: p.reconciled and p.display_type=='payment_term')
        for line in invoice_reconciled_lines:
            reconcile_id = self.env['account.partial.reconcile'].create(line)
            # if line.debit_move_id == invoice_reconciled_line:
            #     reconcile_id = reconcile_obj.create(invoice_reconciled_lines)
    
    def get_reconciled_lines(self, existing_invoice):
        # lines = self.env['account.partial.reconcile'].search([('id','=','0')])
        lines = []
        fields_to_read = [
            'debit_move_id', 'credit_move_id', 'full_reconcile_id', 'exchange_move_id',
            'company_currency_id', 'debit_currency_id', 'credit_currency_id',
            'amount', 'debit_amount_currency', 'credit_amount_currency',
            'company_id', 'max_date'
        ]
        for line in existing_invoice.line_ids.filtered(lambda p: p.reconciled and p.display_type == 'payment_term'):
            reconciled_lines = self.env['account.partial.reconcile'].search(
                ['|', ('credit_move_id', '=', line.id), ('debit_move_id', '=', line.id)])
            for rl in reconciled_lines:
                # Convert each record to a dictionary suitable for creating a new in-memory record
                dict_to_add = {
                    'debit_move_id': rl.debit_move_id.id,
                    'credit_move_id': rl.credit_move_id.id,
                    'company_currency_id': rl.company_currency_id.id,
                    'debit_currency_id': rl.debit_currency_id.id,
                    'credit_currency_id': rl.credit_currency_id.id,
                    'amount': rl.amount,
                    'debit_amount_currency': rl.debit_amount_currency,
                    'credit_amount_currency': rl.credit_amount_currency,
                    'company_id': rl.company_id.id,
                }
                
                # Create a new in-memory record using the dictionary
                # new_record = self.env['account.partial.reconcile'].new(rl_dict)
                lines.append(dict_to_add)
                # if rl.debit_move_id == line.id:
                #     lines += rl.credit_move_id
                # else:
                #     lines += rl.debit_move_id
            # if line.reconciled:
            #     lines += line
        return lines
    
    def get_tax_rate_record(self, parent_cashflow, company):
        tax_cf = self.env['cashflow.controller.bi'].search(
            [('parentcashflowid', '=', parent_cashflow.cashflowid), ('costtype', '=', 'VAT')], limit=1)
        tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode,
                                                                         'purchase', company.id)
        if tax_rate_record:
            return tax_rate_record
    
    def update_existing_line(self, existing_line, company, cf,extended_multiplier, cashflow_lines_all, invoicenumber):
        
        cashflow_id = cashflow_lines_all.search([
            ('invoicenumber', '=', invoicenumber),
            ('payablereceivable', '=', cf['payablereceivable']),
            ('costtype', '=', cf['costtype']),
            ('commodity', '=', cf['commodity']),
            ('material', '=', cf['material']),
            ('erptaxcode', '=', cf['erptaxcode']),
            ('price', '=', cf['price']),
            ('quantityuom', '=', cf['quantityuom'])
        ], limit=1)
        pol = self.env['purchase.order.line']
        if cashflow_id['sectionno']:
            existing_line.fusion_segment_code = cashflow_id['sectionno']
            pol = self.env['purchase.order.line'].search([('fusion_segment_code', '=', cashflow_id['sectionno'])],
                                                         limit=1)
        
        tax_rate_record = self.get_tax_rate_record(cashflow_id, company)
        existing_tax = existing_line.tax_ids
        # if existing_line.move_id.move_type == 'in_refund':
        #     multiplier = -1
        
        if cf['costtype'] == 'Primary Settlement':
            product = self.env['fusion.sync.history'].validate_product(cf['commodity'],
                                                                       cf['material'],
                                                                       cf['quantityuom'])
            uom = self.env['fusion.sync.history'].validate_uom(product,
                                                               cf['quantityuom']
                                                               )
            
            if pol:
                existing_line.purchase_line_id = pol.id
                existing_line.analytic_distribution = pol.analytic_distribution
                existing_analytic = existing_line.analytic_distribution
                existing_line.name = pol.product_id.name
                existing_line.product_id = product.id
                existing_line.product_uom_id = uom.id
                existing_line.quantity = float(cf['quantity'])
                existing_line.price_unit = float(cf['extendedamount'])/ float(cf['quantity'])* extended_multiplier
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
                if tax_rate_record:
                    existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
                else:
                    existing_line.tax_ids = existing_tax
            
            else:
                log_error = self.env['fusion.sync.history.errors'].log_error('InvoiceControllerBI',
                                                                             cashflow_id.invoicenumber,
                                                                             'Purchase order line not found for Primary settlement line',
                                                                             cashflow_id.internalcompany)
                raise UserError('Purchase order line not found for Primary settlement line')
        
        elif cf['costtype'] in ('Pre-payment', 'Provisional Payment',):
            existing_line.product_id = 312,
            existing_line.name = 'Downpayment',
            
            # existing_line.product_uom_id = 1,
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount'] * extended_multiplier)
            existing_analytic = existing_line.analytic_distribution
            if pol:
                # if pol.product_id != existing_line.product_id:
                #     # existing_line.purchase_line_id = [(6, 0, [])]
                existing_line.analytic_distribution = pol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
            
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
        elif cf['costtype'] in ('Pre-payment_Rev', 'Provisional Payment_Rev'):
            existing_line.product_id = 312,
            existing_line.name = 'Downpayment reversal',
            # existing_line.product_uom_id = 1,
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount']) * extended_multiplier
            existing_analytic = existing_line.analytic_distribution
            if pol:
                # if pol.product_id != existing_line.product_id:
                #     existing_line.purchase_line_id = [(6, 0, [])]
                existing_line.analytic_distribution = pol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
            
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
        else:
            cost = self.env['fusion.sync.history'].validate_cost(cf['costtype'])
            existing_line.name = cost.name
            existing_line.product_id = cost.id
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount']) * extended_multiplier
            existing_analytic = existing_line.analytic_distribution
            if pol:
                # if pol.product_id != existing_line.product_id:
                #     existing_line.purchase_line_id = [(6, 0, [])]
                existing_line.analytic_distribution = pol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
                
    def update_existing_si_line(self, existing_line, company, cf, extended_multiplier, invoicenumber):
        cashflow_id = self.env['cashflow.controller.bi'].search([
            ('invoicenumber', '=', invoicenumber),
            ('payablereceivable', '=', cf['payablereceivable']),
            ('costtype', '=', cf['costtype']),
            ('commodity', '=', cf['commodity']),
            ('material', '=', cf['material']),
            ('erptaxcode', '=', cf['erptaxcode']),
            ('price', '=', cf['price']),
            ('quantityuom', '=', cf['quantityuom'])
        ], limit=1)
        sol = self.env['sale.order.line']
        if cashflow_id['sectionno']:
            sol = self.env['sale.order.line'].search([('fusion_segment_code', '=', cashflow_id['sectionno']),
                                                      ('product_id.name', '=', cashflow_id['material'])])
        tax_rate_record = self.get_tax_rate_record(cashflow_id, company)
        existing_tax = existing_line.tax_ids
        
        if cf['costtype'] == 'Primary Settlement':
           
            uom = self.env['fusion.sync.history'].validate_uom(sol.product_id,
                                                               cf['quantityuom']
                                                               )
            
            if sol:
                
                existing_line.name = sol.product_id.name
                existing_line.product_id = sol.product_id.id
                existing_line.product_uom_id = uom.id
                existing_line.quantity = float(cf['quantity'])
                existing_line.price_unit = float(cf['extendedamount'])/ float(cf['quantity']) * extended_multiplier
                # existing_line.purchase_line_id = sol.id
                existing_line.analytic_distribution = sol.analytic_distribution
                existing_analytic = existing_line.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
                existing_line.sale_line_ids = [(4, sol.id)]
                if tax_rate_record:
                    existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
                else:
                    existing_line.tax_ids = existing_tax
            
            else:
                log_error = self.env['fusion.sync.history.errors'].log_error('InvoiceControllerBI',
                                                                             cashflow_id.invoicenumber,
                                                                             'Sale order line not found for Primary settlement line',
                                                                             cashflow_id.internalcompany)
                raise UserError('Related Sale order line not found')
        
        
        elif cf['costtype'] in ('Pre-payment', 'Provisional Payment'):
            
            existing_line.product_id = 312,
            existing_line.name = 'Down payment',
            # existing_line.name = cf[''],
            # existing_line.product_uom_id = 1,
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount'] * extended_multiplier)
            existing_analytic = existing_line.analytic_distribution
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
            if sol:
                if sol.product_id != existing_line.product_id:
                    existing_line.sale_line_ids = [(6, 0, [])]
                # existing_line.purchase_line_id = pol.id
                existing_line.analytic_distribution = sol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
        elif cf['costtype'] in ('Pre-payment_Rev', 'Provisional Payment_Rev'):
            existing_line.product_id = 312,
            existing_line.name = 'Down payment reversal',
            existing_line.product_uom_id = existing_line.product_id.uom_id,
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount']) * extended_multiplier
            existing_analytic = existing_line.analytic_distribution
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
            if sol:
                if sol.product_id != existing_line.product_id:
                    existing_line.sale_line_ids = [(6, 0, [])]
                # existing_line.purchase_line_id = pol.id
                existing_line.analytic_distribution = sol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
        
        
        else:
            if not sol:
                if cashflow_id['sectionno']:
                    sol = self.env['purchase.order.line'].search(
                        [('fusion_segment_code', '=', cashflow_id['sectionno'])])
            cost = self.env['fusion.sync.history'].validate_cost(cf['costtype'])
            existing_line.name = sol.product_id.name if sol else cost.name
            existing_line.product_id = cost.id
            existing_line.quantity = float(1.00)
            existing_line.price_unit = float(cf['extendedamount']) * extended_multiplier
            existing_analytic = existing_line.analytic_distribution
            if tax_rate_record:
                existing_line.tax_ids = [(6, 0, [tax_rate_record.id])]
            else:
                existing_line.tax_ids = existing_tax
            if sol:
                if sol.product_id != existing_line.product_id:
                    existing_line.sale_line_ids = [(6, 0, [])]
                existing_line.analytic_distribution = sol.analytic_distribution
                if existing_analytic:
                    for aa in existing_analytic:
                        existing_line.analytic_distribution[aa] = 100
            
            # primary_cashflows = self.get_cashflow(rec.invoicenumber)
            # for cf in primary_cashflows:
            #     self.update_existing_product_invoice(existing_invoice, cf, po, pol, company)
            # else:
            #     header = self.build_product_invoice_vals(pol, po, company, rec, partner)
            #     related_cfs = self.get_related_partner_segment_cashflows(pol.fusion_segment_code,
            #                                                              'Primary Settlement',
            #                                                              po.partner_id.name)
            #     total_amount = 0
            #     for cf in related_cfs:
            #         total_amount += float(cf.extendedamount*-1)
            #         self.create_product_line(header, pol, cf, company)
            #     # total_amount = sum(line.quantity * line.price_unit for line in header['invoice_line_ids'])
            #     if total_amount > 0:
            #         header['move_type']= 'in_invoice'
            #     elif total_amount < 0:
            #         header['move_type'] = 'in_refund'
            #     new_product_invoice = self.env['account.move'].create(header)
            #     new_product_invoice.action_post()
    
    def update_existing_invoice(self, existing_invoice, cf, po, pol, company):
        existing_invoice.button_draft()
        # link existing invoice
        self.update_existing_invoice_header(existing_invoice, po, pol)
        existing_line = self.env['account.move.line'].search([('cashflow_id', '=', cf.cashflowid)])
        product = self.env['fusion.sync.history'].validate_product(cf.commodity,
                                                                   cf.material,
                                                                   cf.quantityuom)
        
        uom = self.env['fusion.sync.history'].validate_uom(product,
                                                           cf.quantityuom)
        tax_rate_record = self.get_tax_rate_record(cf, company)
        multiplier = 1
        if not cf.payablereceivable == 'Payable':
            multiplier = -1
        if existing_line:
            self.update_existing_product_line(existing_line, cf, pol, tax_rate_record, multiplier)
        else:
            self.create_product_line_existing_invoice(existing_invoice, cf, product, uom, pol, tax_rate_record,
                                                      multiplier, company)
        existing_invoice.action_post()
