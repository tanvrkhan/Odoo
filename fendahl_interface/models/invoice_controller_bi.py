from odoo import models, fields
import requests
import logging

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
                for data in json_data:
                    self.create_update_invoice('invoice', data)
                interface.update_sync_interface('invoice')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_invoice(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('invoice')
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
                for data in json_data:
                    self.regular_update_invoice('invoice', data)
                interface.update_sync_interface('invoice')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_invoice(self, interface_type, data):
        if interface_type == 'invoice':
            exists = self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])])
            if exists:
                return
                # if exists:
                #     return
                # else:
                #     self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
                #     self.env['cashflow.controller.bi'].create(data)
                #     self.env.cr.commit()
            else:
                self.env['invoice.controller.bi'].create(data)
                self.env.cr.commit()
    
    def regular_update_invoice(self, interface_type, data):
        if interface_type == 'invoice':
            exists = self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])])
            if exists:
                self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])]).unlink()
                self.env['invoice.controller.bi'].create(data)
            else:
                self.env['invoice.controller.bi'].create(data)
                self.env.cr.commit()
    
    
    def create_bill(self):
        for rec in self:
            pol = self.env['purchase.order.line'].search([('custom_section_number', '=', rec.customsectionnumber)])
            po = pol.order_id
            # search_pattern = rec.custominvoicenumber[:3] + '%'
            existing_invoice = self.env['account.move'].search([('fusion_invoice_ref', '=', rec.custominvoicenumber)])
            # product=self.env['fusion.sync.history'].validate_product(rec.commodity, rec.material,
            #                                                                                rec.invoiceqtyuom)
            # uom = self.env['fusion.sync.history'].validate_uom(product,
            #                                              rec.invoiceqtyuom)
            if existing_invoice:
                # link existing invoice
                existing_invoice.write({'purchase_id': po.id})
                existing_invoice.write({'invoice_origin': po.name})
                # existing_invoice.write({'custom_section_number': rec.customsectionnumber})
                existing_invoice.line_ids.custom_section_number = rec.customsectionnumber
                
                if rec.invoicestatus == 'Void':
                    existing_invoice.action_cancel()
                elif rec.invoicetype == 'Proforma' or rec.invoicetype == 'Prepayment':
                    invoice_line_vals = {
                        'name': rec.material,
                        'product_id': 312,
                        'product_uom_id': 1,
                        'quantity': 1,
                        'price_unit': rec.invoiceamt if rec.invoiceamt > 0 else rec.invoiceamt * -1,
                        'purchase_line_id': pol.id,
                            'analytic_distribution':pol.analytic_distribution
                        # 'tax_ids': [(6, 0, [tax.id for tax in line.taxes_id])],
                    }
                else:
                    existing_invoice.button_draft()
                    
                    invoice_line_vals = {
                        'name': pol.product_id.name,
                        'product_id': pol.product_id.id,
                        'product_uom_id': pol.product_uom.id,
                        'quantity': rec.invoiceamt / pol.price_unit,
                        'price_unit': pol.price_unit,
                        'purchase_line_id': pol.id,
                            'analytic_distribution':pol.analytic_distribution
                        # 'tax_ids': [(6, 0, [tax.id for tax in line.taxes_id])],
                    }
                    existing_invoice.action_post()
                    
            elif rec.invoicestatus == 'Active' and rec.payablereceivable == 'Payable' and not existing_invoice:
                
                if po:
                    #create new invoice
                    invoice_vals = {
                        'company_id': self.env['res.company'].search([('name', '=', rec.internalcompany)], limit=1).id,
                        'move_type': 'in_invoice',
                        # 'fusion_invoice_ref': rec.invoicenumber, # Vendor bill
                        'invoice_origin': po.name,
                        'partner_id': po.partner_id.id,
                        'invoice_line_ids': [],
                        'currency_id': self.env['res.currency'].search([('name', '=', rec.amtcurrency)], limit=1).id, #po.currency_id.id, # self.env['res.currency'].search([(rec.material)rec.amtcurrency,
                        'purchase_id': po.id,
                        'custom_section_number': rec.customsectionnumber,  # Link back to the purchase order
                        'invoice_date': rec.invoicedate,
                        'date': rec.invoicedate,
                        'ref': rec.theirinvoiceref,
                        'invoice_date_due': rec.paymentduedate,
                        'fusion_reference': rec.invoicenumber,
                        'fusion_invoice_ref' : rec.custominvoicenumber
                        }
                    # product = self.env['fusion.sync.history'].validate_product(rec.material)
                    if rec.invoicetype=='Proforma' or rec.invoicetype=='Prepayment':
                        invoice_line_vals = {
                            'name': pol.product_id.name,
                            'product_id': 312,
                            'product_uom_id': 1,
                            'quantity': 1,
                            'price_unit': rec.invoiceamt if rec.invoiceamt > 0 else rec.invoiceamt*-1,
                            'purchase_line_id': pol.id,
                            'analytic_distribution':pol.analytic_distribution
                            # 'tax_ids': [(6, 0, [tax.id for tax in line.taxes_id])],
                        }
                        invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
                    elif rec.invoicetype=='Final':
                        invoice_line_vals = {
                            'name': pol.product_id.name,
                            'product_id': pol.product_id.id,
                            'product_uom_id': pol.product_uom.id,
                            'quantity': float(rec.invoiceamt if float(rec.invoiceamt) > 0 else float(rec.invoiceamt) * -1)/pol.price_unit,
                            'price_unit': pol.price_unit,
                            'purchase_line_id': pol.id,
                            'analytic_distribution':pol.analytic_distribution
                            # 'tax_ids': [(6, 0, [tax.id for tax in line.taxes_id])],
                        }
                        invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
                    vendor_bill =   self.env['account.move'].create(invoice_vals)
                    vendor_bill.action_post()
                    
                