import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime
from odoo.exceptions import ValidationError


class PostReconciledPayments(models.Model):
    _inherit = 'account.partial.reconcile'
    
    sent_to_fendahl= fields.Boolean("Sent to Sandpit")
    sent_to_fendahl_uat= fields.Boolean("Sent to UAT")
    sent_to_fendahl_prod= fields.Boolean("Sent to Prod")
    debit_move_type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], readonly=True,related='debit_move_id.move_type')
    credit_move_type= fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], readonly=True,related='debit_move_id.move_type')
    
    def action_post_payments(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "268d72e6-5013-4687-8cfa-66d2b633b115"}
        url = "https://kemexonsandpit1.fendahl.in:9002/kemexon/Integration/api/Pyament/CreatePayment"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        for record in self:
            company = ""
            
            match record.debit_move_id.company_id.id:
                case 1:
                    company = "KEMEXON LTD"
                case 2:
                    company = "KEMEXON SA"
                case 4:
                    company = "KEMEXON BRUSSELS SRL"
                case 5:
                    company = "KEMEXON UK LIMITED"
            
            if (record.debit_move_id.move_id.move_type == "out_invoice"):
                if record.debit_move_id.move_id.fusion_reference:
                    invoiceid = record.debit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.credit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.debit_move_id.partner_id.name),
                        "Payment_Made_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.debit_amount_currency,
                        "Payment_Currency": record.emptyFalse(record.debit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.debit_amount_currency,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl = True
                    else:
                        raise ValidationError(response.text)
                else:
                    raise ValidationError("Invoice doesn't have fusion reference")
            elif (self.credit_move_id.move_id.move_type == "in_invoice"):
                if record.credit_move_id.move_id.fusion_reference:
                    invoiceid = record.credit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.debit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.credit_move_id.partner_id.name),
                        "Payment_Made_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.credit_amount_currency*-1,
                        "Payment_Currency": record.emptyFalse(record.credit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.credit_amount_currency*-1,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl = True
                    else:
                        raise ValidationError(response.text)
                    b = 1
                else:
                    raise ValidationError("Invoice doesn't have fusion reference")
    
    def action_post_payments_UAT(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "17e994a0-543b-4384-b173-250b297153ea"}
        url = "https://kemexonuat.fendahl.in:9002/kemexon/Integration/api/Pyament/CreatePayment"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        
        for record in self:
            company = ""
        
            match record.debit_move_id.company_id.id:
                case 1:
                    company = "KEMEXON LTD"
                case 2:
                    company = "KEMEXON SA"
                case 4:
                    company = "KEMEXON BRUSSELS SRL"
                case 5:
                    company = "KEMEXON UK LIMITED"
        
            if (record.debit_move_id.move_id.move_type == "out_invoice"):
                if record.debit_move_id.move_id.fusion_reference:
                    invoiceid = record.debit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.credit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.debit_move_id.partner_id.name),
                        "Payment_Made_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.debit_amount_currency,
                        "Payment_Currency": record.emptyFalse(record.debit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.debit_amount_currency,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl_uat = True
                    else:
                        raise ValidationError(response.text)
                else:
                    raise ValidationError("Invoice doesn't have fusion reference")
            elif (self.credit_move_id.move_id.move_type == "in_invoice"):
                if record.credit_move_id.move_id.fusion_reference:
                    invoiceid = record.credit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.debit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.credit_move_id.partner_id.name),
                        "Payment_Made_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.credit_amount_currency,
                        "Payment_Currency": record.emptyFalse(record.credit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.credit_amount_currency,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl_uat = True
                    else:
                        raise ValidationError(response.text)
                    b = 1
                else:
                    raise ValidationError("Invoice doesn't have fusion reference")
    def action_post_payments_Prod(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "51a029bb-2e98-4f85-a9e0-194e315f39f7"}
        url = "https://kemexonprod.fendahl.in:9002/kemexon/Integration/api/Pyament/CreatePayment"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        for record in self:
            company = ""
            match record.debit_move_id.company_id.id:
                case 1:
                    company = "KEMEXON LTD"
                case 2:
                    company = "KEMEXON SA"
                case 4:
                    company = "KEMEXON BRUSSELS SRL"
                case 5:
                    company = "KEMEXON UK LIMITED"
            
            if (record.debit_move_id.move_id.move_type == "out_invoice"):
                if record.debit_move_id.move_id.fusion_reference:
                    invoiceid = record.debit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.credit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.debit_move_id.partner_id.name),
                        "Payment_Made_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.credit_move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.debit_amount_currency,
                        "Payment_Currency": record.emptyFalse(record.debit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.debit_amount_currency,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl_prod = True
                        a = 1
                    else:
                        raise ValidationError(response.text)
                else:
                    raise ValidationError("Invoice doesn't have fusion reference")
            elif (self.credit_move_id.move_id.move_type == "in_invoice"):
                if record.credit_move_id.move_id.fusion_reference:
                    invoiceid = record.credit_move_id.move_id.fusion_reference.split(",")[0]
                    json_data = {
                        "Accounting_System_Payment_ID": record.debit_move_id.id,
                        "Internal_Company_Code": company,
                        "CounterParty_Code": record.emptyFalse(record.credit_move_id.partner_id.name),
                        "Payment_Made_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Due_Date": record.debit_move_id.move_id.date.strftime("%d-%m-%Y"),
                        "Payment_Amount": record.credit_amount_currency,
                        "Payment_Currency": record.emptyFalse(record.credit_currency_id.name),
                        "Payment_Allocations": [
                            {
                                "Invoice_Master_ID": record.emptyFalse(invoiceid),
                                "Allocated_Amount": record.credit_amount_currency,
                            }
                        ],
                        
                    }
                    response = requests.post(url, data=json.dumps(json_data), headers=headers)
                    if (response.status_code == 200):
                        record.sent_to_fendahl_prod = True
                    else:
                        raise ValidationError(response.text)
                else:
                    raise ValidationError("Invoice reference not found")
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))
    
    def emptyFalse(self,value):
        if value:
            return value
        else:
            return ''