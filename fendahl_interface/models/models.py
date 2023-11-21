import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser


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
    _inherit = 'account.full.reconcile'
    
    def action_post_payments(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "268d72e6-5013-4687-8cfa-66d2b633b115"}
        url = "https://kemexonsandpit1.fendahl.in:9002/kemexon/Integration/api/Company/CreateCompany"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        isactive = False
        match self.status:
            case "approved":
                isactive = True
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
            "Sanctioned": "Un Blocked",
            "GL_Code": self.id,
            "GL_Customer_Code": self.property_account_receivable_id.code,
            "GL_Vendor_Code": self.property_account_payable_id.code,
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