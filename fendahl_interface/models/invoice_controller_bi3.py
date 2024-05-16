# from odoo import models, fields
# import requests
# import logging
# from odoo.exceptions import UserError, Warning
#
# _logger = logging.getLogger(__name__)
# class InvoiceControllerBI(models.Model):
#     _name = 'invoice.controller.bi'
#     _description = 'Invoice Controller Business Intelligence'
#
#     invoicenumber = fields.Integer(string="InvoiceNumber")
#     provisionalenum = fields.Char(string="ProvisionalEnum")
#     invoicedate = fields.Char(string="InvoiceDate")
#     paymentduedate = fields.Char(string="PaymentDueDate")
#     counterparty = fields.Char(string="Counterparty")
#     internalcompany = fields.Char(string="InternalCompany")
#     commodity = fields.Char(string="Commodity")
#     location = fields.Char(string="Location")
#     invoiceamt = fields.Char(string="InvoiceAmt")
#     paidamt = fields.Char(string="PaidAmt")
#     openamt = fields.Char(string="OpenAmt")
#     paidreceived = fields.Char(string="PaidReceived")
#     amtcurrency = fields.Char(string="AmtCurrency")
#     ourinvoiceref = fields.Char(string="OurInvoiceRef")
#     theirinvoiceref = fields.Char(string="TheirInvoiceRef")
#     invoicestatus = fields.Char(string="InvoiceStatus")
#     fullypaiddate = fields.Char(string="FullyPaidDate")
#     lastpaymentdate = fields.Char(string="LastPaymentDate")
#     refcurrency = fields.Char(string="RefCurrency")
#     currencyindexentry = fields.Char(string="CurrencyIndexEntry")
#     venture = fields.Char(string="Venture")
#     actperiodcode = fields.Char(string="ActPeriodCode")
#     paymentmethod = fields.Char(string="PaymentMethod")
#     transmitstatus = fields.Char(string="TransmitStatus")
#     paymentid = fields.Char(string="PaymentId")
#     displayinvoiceid = fields.Char(string="DisplayInvoiceId")
#     ourpaymentinstr = fields.Char(string="OurPaymentInstr")
#     theirpaymentinstr = fields.Char(string="TheirPaymentInstr")
#     paymentreleasedate = fields.Char(string="PaymentReleaseDate")
#     payablereceivable = fields.Char(string="PayableReceivable")
#     postingdate = fields.Char(string="PostingDate")
#     strategycode = fields.Char(string="StrategyCode")
#     originlocation = fields.Char(string="OriginLocation")
#     gradecategory = fields.Char(string="GradeCategory")
#     mot = fields.Char(string="Mot")
#     sapactperiod = fields.Char(string="SapActPeriod")
#     sappostingdate = fields.Char(string="SapPostingDate")
#     currentaccountingperiod = fields.Char(string="CurrentAccountingPeriod")
#     billtoparty = fields.Char(string="BillToParty")
#     payer = fields.Char(string="Payer")
#     shiptoparty = fields.Char(string="ShipToParty")
#     invoicepresentedby = fields.Char(string="InvoicePresentedBy")
#     invoicecreatedby = fields.Char(string="InvoiceCreatedBy")
#     blockedforpayment = fields.Char(string="BlockedForPayment")
#     adjustedduedate = fields.Char(string="AdjustedDueDate")
#     isfinanciallysettled = fields.Char(string="IsFinanciallySettled")
#     approver1 = fields.Char(string="Approver1")
#     approver2 = fields.Char(string="Approver2")
#     invoiceopenstatus = fields.Char(string="InvoiceOpenStatus")
#     displayinvoice = fields.Char(string="DisplayInvoice")
#     accountingperioddate = fields.Char(string="AccountingPeriodDate")
#     postingstatusenum = fields.Char(string="PostingStatusEnum")
#     postingneededstatusenum = fields.Char(string="PostingNeededStatusEnum")
#     batchprocessid = fields.Char(string="BatchProcessId")
#     basecurrency = fields.Char(string="BaseCurrency")
#     reportingcurrency = fields.Char(string="ReportingCurrency")
#     invoiceamtbasecurrency = fields.Char(string="InvoiceAmtBaseCurrency")
#     invoiceamtreportingcurrency = fields.Char(string="InvoiceAmtReportingCurrency")
#     externalreferencenumber = fields.Char(string="ExternalReferenceNumber")
#     masterdealid = fields.Char(string="MasterDealId")
#     referencenumber = fields.Char(string="ReferenceNumber")
#     ispledgedtobank = fields.Boolean(string="IsPledgedToBank")
#     productdescription = fields.Char(string="ProductDescription")
#     paymentstatus = fields.Char(string="PaymentStatus")
#     counterpartylevelinstrument = fields.Char(string="CounterpartyLevelInstrument")
#     invoicetype = fields.Char(string="InvoiceType")
#     fxrate = fields.Char(string="FxRate")
#     navpostingdate = fields.Char(string="NavPostingDate")
#     invoicecreationdate = fields.Char(string="InvoiceCreationDate")
#     taxclausedetailcode = fields.Char(string="TaxClauseDetailCode")
#     taxclausedescription = fields.Char(string="TaxClauseDescription")
#     postinggroup = fields.Char(string="PostingGroup")
#     allocatedamount = fields.Char(string="AllocatedAmount")
#     openallocation = fields.Char(string="OpenAllocation")
#     businessunit = fields.Char(string="BusinessUnit")
#     overrideextendedamount = fields.Char(string="OverrideExtendedAmount")
#     isoverrideextendedamount = fields.Char(string="IsOverrideExtendedAmount")
#     counterpartname = fields.Char(string="CounterpartName")
#     issegmentfinal = fields.Char(string="IsSegmentFinal")
#     parentinvoiceid = fields.Char(string="ParentInvoiceId")
#     countryoforigin = fields.Char(string="CountryOfOrigin")
#     countryofload = fields.Char(string="CountryOfLoad")
#     countryofdischarge = fields.Char(string="CountryOfDischarge")
#     isanimalfeed = fields.Boolean(string="IsAnimalFeed")
#     reachcategory = fields.Char(string="ReachCategory")
#     cropyear = fields.Char(string="CropYear")
#     variety = fields.Char(string="Variety")
#     titletransferlocation = fields.Char(string="TitleTransferLocation")
#     netting = fields.Char(string="Netting")
#     vehiclemottype = fields.Char(string="VehicleMotType")
#     intapprovedperson = fields.Char(string="IntApprovedPerson")
#     extapprovedperson = fields.Char(string="ExtApprovedPerson")
#     navpackageid = fields.Char(string="NavPackageId")
#     navinvoiceid = fields.Char(string="NavInvoiceId")
#     packagingcode = fields.Char(string="PackagingCode")
#     licensecode = fields.Char(string="LicenseCode")
#     specificationcode = fields.Char(string="SpecificationCode")
#     mirrorinvoicemasterid = fields.Char(string="MirrorInvoiceMasterId")
#     transfercommencementdate = fields.Char(string="TransferCommencementDate")
#     invoiceraisedon = fields.Char(string="InvoiceRaisedOn")
#     isallocatetolc = fields.Boolean(string="IsAllocateToLc")
#     weightfinalat = fields.Char(string="WeightFinalAt")
#     custominvoicenumber = fields.Char(string="CustomInvoiceNumber")
#     cpdate = fields.Char(string="CpDate")
#     vessel = fields.Char(string="Vessel")
#     material = fields.Char(string="Material")
#     accountpaymentstatust = fields.Char(string="AccountPaymentStatust")
#     invoicecategory = fields.Char(string="InvoiceCategory")
#     isattachmentavailable = fields.Char(string="IsAttachmentAvailable")
#     isnotesavailable = fields.Char(string="IsNotesAvailable")
#     book = fields.Char(string="Book")
#     positionstatus = fields.Char(string="PositionStatus")
#     writeoffamt = fields.Char(string="WriteOffAmt")
#     customtradenumber = fields.Char(string="CustomTradeNumber")
#     customsectionnumber = fields.Char(string="CustomSectionNumber")
#     quantity = fields.Char(string="Quantity")
#     erppostingdate = fields.Char(string="ErpPostingDate")
#     erpaccountingperiod = fields.Char(string="ErpAccountingPeriod")
#     invoiceqtyuom = fields.Char(string="InvoiceQtyUom")
#     ispaymentdueoverridden = fields.Char(string="IsPaymentDueOverridden")
#     invoicelinkid = fields.Char(string="InvoiceLinkId")
#     refinvoiceid = fields.Char(string="RefInvoiceId")
#     refcustominvoiceid = fields.Char(string="RefCustomInvoiceId")
#     letterofcredit = fields.Char(string="LetterOfCredit")
#     certificateno = fields.Char(string="CertificateNo")
#     taxcurrency = fields.Char(string="TaxCurrency")
#     invoiceamttaxccyexcl = fields.Char(string="InvoiceAmtTaxCcyExcl")
#     invoiceamttaxccyincl = fields.Char(string="InvoiceAmtTaxCcyIncl")
#     taxamttaxccy = fields.Char(string="TaxAmtTaxCcy")
#     samplerequired = fields.Char(string="SampleRequired")
#     samplingprocess = fields.Char(string="SamplingProcess")
#     ourvatnumber = fields.Char(string="OurVatNumber")
#     theirvatnumber = fields.Char(string="TheirVatNumber")
#     companycategory = fields.Char(string="CompanyCategory")
#     arbitrationcode = fields.Char(string="ArbitrationCode")
#     periodtype = fields.Char(string="PeriodType")
#     docclassification = fields.Char(string="DocClassification")
#     writeoffamount = fields.Char(string="WriteOffAmount")
#     writeoffamountcurrency = fields.Char(string="WriteOffAmountCurrency")
#     invoicevaluedate = fields.Char(string="InvoiceValueDate")
#     isgeneratecost = fields.Char(string="IsGenerateCost")
#     origin = fields.Char(string="Origin")
#     portfolio = fields.Char(string="Portfolio")
#     grade = fields.Char(string="Grade")
#     invoiceamountexcltax = fields.Char(string="InvoiceAmountExclTax")
#     invoiceamountinctax = fields.Char(string="InvoiceAmountIncTax")
#     taxamount = fields.Char(string="TaxAmount")
#     operator = fields.Char(string="Operator")
#     writeoffdate = fields.Char(string="WriteOffDate")
#     invoicereference = fields.Char(string="InvoiceReference")
#     isadjusted = fields.Boolean(string="IsAdjusted")
#     transportcarriage = fields.Char(string="TransportCarriage")
#     transportcarriagecode = fields.Char(string="TransportCarriageCode")
#     ismigrated = fields.Char(string="IsMigrated")
#     paymentcurrency = fields.Char(string="PaymentCurrency")
#     tradelinkcode = fields.Char(string="TradeLinkCode")
#     tradelinkid = fields.Char(string="TradeLinkId")
#     lockid = fields.Integer(string="LockId")
#     statusenum = fields.Char(string="StatusEnum")
#     modifypersonid = fields.Char(string="ModifyPersonId")
#     modifyperson = fields.Char(string="ModifyPerson")
#     lastmodifydate = fields.Char(string="LastModifyDate")
#     customerid = fields.Char(string="CustomerId")
#     birecordcreationdate = fields.Char(string="BiRecordCreationDate")
#
#     def import_invoice(self):
#         interface = self.env['fusion.sync.history']
#         last_sync = '2023-01-01'
#         url = "https://fusionsqlmirrorapi.azure-api.net/api/invoice"
#         headers = {
#             'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
#             'Content-Type': 'application/json',
#         }
#         params = {
#             'date': last_sync
#         }
#
#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code == 200:
#             try:
#                 json_data = response.json()
#                 json_data = interface.lowercase_keys(json_data)
#                 for data in json_data:
#                     self.create_update_invoice('invoice', data)
#                 interface.update_sync_interface('invoice')
#             except Exception as e:
#                 _logger.error('Error processing API data: %s', str(e))
#         else:
#             _logger.error('Failed to fetch data from external API: %s', response.status_code)
#
#     def sync_invoice(self):
#         interface = self.env['fusion.sync.history']
#         last_sync = interface.get_last_sync('invoice')
#         url = "https://fusionsqlmirrorapi.azure-api.net/api/invoice"
#         headers = {
#             'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
#             'Content-Type': 'application/json',
#         }
#         params = {
#             'date': last_sync
#         }
#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code == 200:
#             try:
#                 json_data = response.json()
#                 json_data = interface.lowercase_keys(json_data)
#                 for data in json_data:
#                     self.regular_update_invoice('invoice', data)
#                 interface.update_sync_interface('invoice')
#             except Exception as e:
#                 _logger.error('Error processing API data: %s', str(e))
#         else:
#             _logger.error('Failed to fetch data from external API: %s', response.status_code)
#
#     def create_update_invoice(self, interface_type, data):
#         if interface_type == 'invoice':
#             exists = self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])])
#             if exists:
#                 return
#                 # if exists:
#                 #     return
#                 # else:
#                 #     self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
#                 #     self.env['cashflow.controller.bi'].create(data)
#                 #     self.env.cr.commit()
#             else:
#                 self.env['invoice.controller.bi'].create(data)
#                 self.env.cr.commit()
#
#     def regular_update_invoice(self, interface_type, data):
#         if interface_type == 'invoice':
#             exists = self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])])
#             if exists:
#                 self.env['invoice.controller.bi'].search([('invoicenumber', '=', data['invoicenumber'])]).unlink()
#                 self.env['invoice.controller.bi'].create(data)
#             else:
#                 self.env['invoice.controller.bi'].create(data)
#                 self.env.cr.commit()
#
#     def create_bill(self):
#         for rec in self:
#             try:
#                 if rec.payablereceivable == 'Payable':
#                     pol = self.env['purchase.order.line'].search([('custom_section_number', '=', rec.customsectionnumber)])
#                     po = pol.order_id
#                     cashflow = self.get_cashflow(pol.fusion_segment_code)
#                     company = self.get_company(rec.internalcompany)
#
#                     if rec.invoicestatus == 'Active':
#                         self.process_active_invoice(rec, pol, po, cashflow, company)
#                     else:
#                         self.cancel_invoice(rec.customsectionnumber)
#             except Exception as e:
#                 self.log_error('TransferController', rec.invoicenumber, str(e), rec.internalcompany)
#                 raise UserError(f'Error processing API data: {e}')
#
#     def get_cashflow(self, segment_code):
#         return self.env['cashflow.controller.bi'].search([
#             ('sectionno', '=', segment_code),
#             ('cashflowstatus', '!=', 'Defunct'),
#             ('quantitystatus', '=', 'Actual')
#         ])
#
#     def get_company(self, company_name):
#         return self.env['res.company'].search([('name', '=', company_name)], limit=1)
#
#     def process_active_invoice(self, rec, pol, po, cashflow, company):
#         for cf in cashflow:
#             if cf.costtype == 'Primary Settlement':
#                 existing_invoice = self.env['account.move'].search([
#                     ('fusion_segment_code', '=', pol.fusion_segment_code),
#                     ('partner_id', '=', pol.partner_id.id)
#                 ])
#                 self.handle_invoice(existing_invoice, cf, pol, po, company, rec)
#
#     def handle_invoice(self, invoice, cf, pol, po, company, rec):
#         if invoice:
#             self.update_invoice(invoice, pol, po)
#             self.manage_invoice_lines(cf, pol, company, invoice)
#             invoice.action_post()
#         else:
#             self.create_new_invoice(cf, pol, po, company, rec)
#
#     def update_invoice(self, invoice, pol, po):
#         invoice.button_draft()
#         self.env.cr.commit()
#         invoice.write({
#             'purchase_id': po.id,
#             'invoice_origin': po.name,
#             'fusion_segment_code': pol.fusion_segment_code,
#             'fusion_segment_id': pol.fusion_segment_id
#         })
#
#     def manage_invoice_lines(self, cf, pol, company, invoice):
#         tax_cf = self.env['cashflow.controller.bi'].search(
#             [('parentcashflowid', '=', cf.cashflowid), ('costtype', '=', 'VAT')], limit=1)
#         tax_rate_record = self.env['fusion.sync.history'].get_tax_record(tax_cf.erptaxcode, 'purchase', company.id)
#         existing_line = self.env['account.move.line'].search([('cashflow_id', '=', cf.cashflowid)])
#         product, uom = self.validate_product_and_uom(cf.commodity, cf.material, cf.quantityuom)
#
#         multiplier = 1 if cf.payablereceivable == 'Payable' else -1
#         if existing_line:
#             self.update_existing_line(existing_line, pol, product, uom, cf, multiplier, tax_rate_record)
#         else:
#             self.create_new_line(invoice, pol, product, uom, cf, multiplier, tax_rate_record)
#
#     def create_new_invoice(self, cf, pol, po, company, rec):
#         move_type = 'in_invoice' if rec.invoicetype in ["Final", "Service Cost Invoice"] and float(rec.invoiceamt) >= 0 else 'in_refund'
#         invoice_vals = self.build_invoice_vals(pol, po, company, rec, move_type)
#         vendor_bill = self.env['account.move'].create(invoice_vals)
#         vendor_bill.action_post()
#
#     def update_existing_line(self, line, pol, product, uom, cf, multiplier, tax_rate_record):
#         line.update({
#             'name': pol.product_id.name,
#             'product_id': product.id,
#             'product_uom_id': uom.id,
#             'quantity': float(cf.quantity),
#             'price_unit': cf.price * multiplier,
#             'purchase_line_id': pol.id,
#             'analytic_distribution': pol.analytic_distribution,
#             'taxes_id': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])]
#         })
#
#     def create_new_line(self, invoice, pol, product, uom, cf, multiplier, tax_rate_record):
#         self.env['account.move.line'].create({
#             'move_id': invoice.id,
#             'name': pol.product_id.name,
#             'product_id': product.id,
#             'product_uom_id': uom.id,
#             'quantity': float(cf.quantity),
#             'price_unit': float(cf.price) * multiplier,
#             'purchase_line_id': pol.id,
#             'analytic_distribution': pol.analytic_distribution,
#             'cashflow_id': cf.cashflowid,
#             'tax_ids': [(6, 0, [tax_rate_record.id])] if tax_rate_record else [(6, 0, [])]
#         })
#
#     def cancel_invoice(self, custom_section_number):
#         cancelled_invoice = self.env['account.move'].search([('custom_section_number', '=', custom_section_number)])
#         if cancelled_invoice:
#             cancelled_invoice.action_cancel()
#
#     def log_error(self, controller_name, invoice_number, error_message, company):
#         return self.env['fusion.sync.history.errors'].log_error(controller_name, invoice_number, error_message, company)
#
#     def build_invoice_vals(self, pol, po, company, rec, move_type,partner):
#         return {
#             'company_id': company.id,
#             'invoice_origin': po.name,
#             'partner_id': partner.id,
#             'invoice_line_ids': [],
#             'currency_id': self.env['res.currency'].search([('name', '=', rec.amtcurrency)], limit=1).id,
#             'purchase_id': po.id,
#             'custom_section_number': rec.customsectionnumber,
#             'invoice_date': rec.invoicedate,
#             'date': rec.invoicedate,
#             'ref': rec.theirinvoiceref,
#             'invoice_date_due': rec.paymentduedate,
#             'fusion_reference': rec.invoicenumber,
#             'fusion_invoice_ref': rec.custominvoicenumber,
#             'move_type': move_type
#         }
#
#     def validate_product_and_uom(self, commodity, material, quantityuom):
#         product = self.env['fusion.sync.history'].validate_product(commodity, material, quantityuom)
#         uom = self.env['fusion.sync.history'].validate_uom(product, quantityuom)
#         return product, uom