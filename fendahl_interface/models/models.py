import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime

class PostContactsModel(models.Model):
    _inherit = 'res.partner'
    
    def action_post_contacts(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache","Apikey": "268d72e6-5013-4687-8cfa-66d2b633b115"}
        url = "https://kemexonsandpit1.fendahl.in:9002/kemexon/Integration/api/Company/CreateCompany"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        isactive= False
        match self.status:
            case "approved":
                isactive=True
        json_data = {
            "Code": self.display_name,
            "Config_code": self.short_name,
            "Name": self.name,
            "Company_Type": "counterpart",
            "Legal_Name": self.name,
            "Is_Kyc_Done": isactive,
            "Active": isactive,
            "External_Ref": self.x_studio_quick_name,
            # "Payment_Term": record.property_payment_term_id.name,
            "Is_Deleted": False,
            "Sanctioned":"Un Blocked",
            "GL_Code":self.id,
            "GL_Customer_Code": self.property_account_receivable_id.code,
            "GL_Vendor_Code":self.property_account_payable_id.code,
            "Company_Address_Models": [
                {
                    "Address_Type": self.type,
                    "Address_Line1": self.street,
                    "Contact_Person": "",
                    "City_Name": self.city,
                    "Country": self.country_id.name,
                    "County": self.state_id.name,
                    "Phone": self.phone,
                    "Mobile_Number": self.mobile
                }
            ]
        }
        
        response = requests.post(url, data=json.dumps(json_data), headers=headers)


class PostReconciledPayments(models.Model):
    _inherit = 'account.partial.reconcile'
    
    sent_to_fendahl= fields.Boolean("Sent to Fendahl")
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
        company=""
        match self.debit_move_id.company_id.id:
            case 1:
                company="KEMEXON LTD"
            case 2:
                company = "KEMEXON SA"
            case 4:
                company = "KEMEXON BRUSSELS SRL"
            case 5:
                company = "KEMEXON UK LIMITED"
            
        if(self.debit_move_id.move_type=="out_invoice"):
            json_data = {
                "Accounting_System_Payment_ID": self.credit_move_id.id,
                "Internal_Company_Code": company,
                "CounterParty_Code": self.debit_move_id.partner_id.name,
                "Payment_Made_Date": self.credit_move_id.date.strftime("%d-%m-%Y"),
                "Payment_Due_Date": self.credit_move_id.date.strftime("%d-%m-%Y"),
                "Payment_Amount": self.credit_move_id.balance*-1,
                "Payment_Currency": self.credit_move_id.currency_id.name,
                "Payment_Allocations": [
                    {
                        "Invoice_Master_ID": self.debit_move_id.move_id.fusion_reference,
                        "Allocated_Amount": self.amount,
                    }
                ],
                
            }
            response = requests.post(url, data=json.dumps(json_data), headers=headers)
            if(response.status_code==200):
                self.sent_to_fendahl=True
            a=1
        elif (self.credit_move_id.move_type == "in_invoice"):
            json_data = {
                "Accounting_System_Payment_ID": self.debit_move_id.id,
                "Internal_Company_Code": company,
                "CounterParty_Code": self.credit_move_id.partner_id.name,
                "Payment_Made_Date": self.debit_move_id.move_id.date.isoformat(),
                "Payment_Due_Date": self.debit_move_id.move_id.date.isoformat(),
                "Payment_Amount": self.debit_move_id.balance,
                "Payment_Currency": self.debit_move_id.currency_id.name,
                "Payment_Allocations": [
                    {
                        "Invoice_Master_ID": self.credit_move_id.move_id.fusion_reference,
                        "Allocated_Amount": self.amount,
                    }
                ],
                
            }
            response = requests.post(url, data=json.dumps(json_data), headers=headers)
            if (response.status_code == 200):
                self.sent_to_fendahl = True
            b=1
    
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))