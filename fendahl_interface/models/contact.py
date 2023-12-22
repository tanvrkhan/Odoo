import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime
from odoo.exceptions import ValidationError


class PostContactsModel(models.Model):
    _inherit = 'res.partner'

    sent_to_fendahl_sandpit = fields.Boolean()
    sent_to_fendahl_uat = fields.Boolean()
    sent_to_fendahl_prod = fields.Boolean()
    message_fendahl_sandpit = fields.Char()
    message_fendahl_uat = fields.Char()
    message_fendahl_prod = fields.Char()

    def action_post_contacts(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "268d72e6-5013-4687-8cfa-66d2b633b115"}
        url = "https://kemexonsandpit1.fendahl.in:9002/kemexon/Integration/api/Company/CreateCompany"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        for record in self:
            isactive = False
            match record.status:
                case "approved":
                    isactive = True
            json_data = {
                "Code": record.emptyFalse(record.display_name),
                "Config_code": record.emptyFalse(record.short_name),
                "Name": record.emptyFalse(record.name),
                "Company_Type": "counterpart",
                "Legal_Name": record.emptyFalse(record.name),
                "Is_Kyc_Done": isactive,
                "Active": isactive,
                "External_Ref": record.emptyFalse(record.x_studio_quick_name),
                # "Payment_Term": record.property_payment_term_id.name,
                "Is_Deleted": False,
                "Sanctioned": "Un Blocked",
                "GL_Code": record.id,
                "GL_Customer_Code": record.emptyFalse(record.property_account_receivable_id.code),
                "GL_Vendor_Code": record.emptyFalse(record.property_account_payable_id.code),
                "Company_Address_Models": [
                    {
                        "Address_Type": record.emptyFalse(record.type),
                        "Address_Line1": record.emptyFalse(record.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(record.city),
                        "Country": record.emptyFalse(record.country_id.name),
                        "County": record.emptyFalse(record.state_id.name),
                        "Phone": record.emptyFalse(record.phone),
                        "Mobile_Number": record.emptyFalse(record.mobile)
                    }
                ]
            }
            altaddresses = record.env['res.partner'].search([('parent_id', '=', record.id)])
            if altaddresses:
                for address in altaddresses:
                    new_address = {
                        "Address_Type": record.emptyFalse(address.type),
                        "Address_Line1": record.emptyFalse(address.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(address.city),
                        "Country": record.emptyFalse(address.country_id.name),
                        "County": record.emptyFalse(address.state_id.name),
                        "Phone": record.emptyFalse(address.phone),
                        "Mobile_Number": record.emptyFalse(address.mobile)
                    }
                    json_data['Company_Address_Models'].append(new_address)

            response = requests.post(url, data=json.dumps(json_data), headers=headers)
            if (response.status_code != 200):
                record.message_fendahl_sandpit = response.text
                record.sent_to_fendahl_sandpit = False
                raise ValidationError(record.name + response.text)
            else:
                record.sent_to_fendahl_sandpit = True

    def action_post_contacts_uat(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                   "Apikey": "17e994a0-543b-4384-b173-250b297153ea"}
        url = "https://kemexonuat.fendahl.in:9002/kemexon/Integration/api/Company/CreateCompany"
        # params = {
        #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
        #     # Add other parameters if required by the API
        # }
        for record in self:
            isactive = False
            match record.status:
                case "approved":
                    isactive = True
            json_data = {
                "Code": record.emptyFalse(record.display_name),
                "Config_code": record.emptyFalse(record.short_name),
                "Name": record.emptyFalse(record.name),
                "Company_Type": "counterpart",
                "Legal_Name": record.emptyFalse(record.name),
                "Is_Kyc_Done": isactive,
                "Active": isactive,
                "External_Ref": record.emptyFalse(record.x_studio_quick_name),
                # "Payment_Term": record.property_payment_term_id.name,
                "Is_Deleted": False,
                "Sanctioned": "Un Blocked",
                "GL_Code": record.id,
                "GL_Customer_Code": record.emptyFalse(record.property_account_receivable_id.code),
                "GL_Vendor_Code": record.emptyFalse(record.property_account_payable_id.code),
                "Company_Address_Models": [
                    {
                        "Address_Type": record.emptyFalse(record.type),
                        "Address_Line1": record.emptyFalse(record.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(record.city),
                        "Country": record.emptyFalse(record.country_id.name),
                        "County": record.emptyFalse(record.state_id.name),
                        "Phone": record.emptyFalse(record.phone),
                        "Mobile_Number": record.emptyFalse(record.mobile)
                    },
                ]
            }
            altaddresses = record.env['res.partner'].search([('parent_id', '=', record.id)])
            if altaddresses:
                for address in altaddresses:
                    new_address = {
                        "Address_Type": record.emptyFalse(address.type),
                        "Address_Line1": record.emptyFalse(address.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(address.city),
                        "Country": record.emptyFalse(address.country_id.name),
                        "County": record.emptyFalse(address.state_id.name),
                        "Phone": record.emptyFalse(address.phone),
                        "Mobile_Number": record.emptyFalse(address.mobile)
                    }
                    json_data['Company_Address_Models'].append(new_address)

            response = requests.post(url, data=json.dumps(json_data), headers=headers)
            if (response.status_code != 200):
                record.message_fendahl_uat = response.text
                record.sent_to_fendahl_uat = False
                raise ValidationError(record.name + response.text)
            else:
                record.sent_to_fendahl_uat = True

    def action_post_contacts_prod(self):
        for record in self:
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
                       "Apikey": "51a029bb-2e98-4f85-a9e0-194e315f39f7"}
            url = "https://kemexonprod.fendahl.in:9002/kemexon/Integration/api/Company/CreateCompany"
            # params = {
            #     "api_key": "268d72e6-5013-4687-8cfa-66d2b633b115",
            #     # Add other parameters if required by the API
            # }
            isactive = False
            match record.status:
                case "approved":
                    isactive = True
            json_data = {
                "Code": record.emptyFalse(record.display_name),
                "Config_code": record.emptyFalse(record.short_name),
                "Name": record.emptyFalse(record.name),
                "Company_Type": "counterpart",
                "Legal_Name": record.emptyFalse(record.name),
                "Is_Kyc_Done": isactive,
                "Active": isactive,
                "External_Ref": record.emptyFalse(record.x_studio_quick_name),
                # "Payment_Term": record.property_payment_term_id.name,
                "Is_Deleted": False,
                "Sanctioned": "Un Blocked",
                "GL_Code": record.id,
                "GL_Customer_Code": record.emptyFalse(record.property_account_receivable_id.code),
                "GL_Vendor_Code": record.emptyFalse(record.property_account_payable_id.code),
                "Company_Address_Models": [
                    {
                        "Address_Type": record.emptyFalse(record.type),
                        "Address_Line1": record.emptyFalse(record.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(record.city),
                        "Country": record.emptyFalse(record.country_id.name),
                        "County": record.emptyFalse(record.state_id.name),
                        "Phone": record.emptyFalse(record.phone),
                        "Mobile_Number": record.emptyFalse(record.mobile)
                    }
                ]
            }
            altaddresses = record.env['res.partner'].search([('parent_id', '=', record.id)])
            if altaddresses:
                for address in altaddresses:
                    new_address = {
                        "Address_Type": record.emptyFalse(address.type),
                        "Address_Line1": record.emptyFalse(address.street),
                        "Contact_Person": "",
                        "City_Name": record.emptyFalse(address.city),
                        "Country": record.emptyFalse(address.country_id.name),
                        "County": record.emptyFalse(address.state_id.name),
                        "Phone": record.emptyFalse(address.phone),
                        "Mobile_Number": record.emptyFalse(address.mobile)
                    }
                    json_data['Company_Address_Models'].append(new_address)
            response = requests.post(url, data=json.dumps(json_data), headers=headers)
            if (response.status_code != 200):
                record.message_fendahl_prod = response.text
                record.sent_to_fendahl_prod = False
                raise ValidationError(record.name + response.text)
            else:
                record.sent_to_fendahl_prod = True

    def emptyFalse(self, value):
        if value:
            return value
        else:
            return ''