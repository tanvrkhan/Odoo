from odoo import models, fields
import requests
import logging

_logger = logging.getLogger(__name__)
class NominationControllerBI(models.Model):
    _name = 'nomination.controller.bi'
    _description = 'Nomination Controller Business Intelligence'
    
    nominationcontrollerbiid = fields.Integer(string="NominationControllerBiId")
    itineraryid = fields.Char(string="ItineraryId")
    itineraryname = fields.Char(string="ItineraryName")
    itinerarystatusenum = fields.Char(string="ItineraryStatusEnum")
    movementid = fields.Char(string="MovementId")
    mottypeenum = fields.Char(string="MotTypeEnum")
    motid = fields.Char(string="MotId")
    motcode = fields.Char(string="MotCode")
    departlocationcode = fields.Char(string="DepartLocationCode")
    arrivelocationcode = fields.Char(string="ArriveLocationCode")
    departdate = fields.Char(string="DepartDate")
    arrivedate = fields.Char(string="ArriveDate")
    itinerarytypeenum = fields.Char(string="ItineraryTypeEnum")
    materialid = fields.Char(string="MaterialId")
    transportcarriagetypeenum = fields.Char(string="TransportCarriageTypeEnum")
    intercompenum = fields.Char(string="InterCompEnum")
    nominationnumber = fields.Char(string="NominationNumber")
    sapdocumentid = fields.Char(string="SapDocumentId")
    sapstatusenum = fields.Char(string="SapStatusEnum")
    nominationkey = fields.Char(string="NominationKey")
    isfinalized = fields.Char(string="IsFinalized")
    finalizeddate = fields.Char(string="FinalizedDate")
    isfinalizedmovement = fields.Char(string="IsFinalizedMovement")
    finalizeddatemovement = fields.Char(string="FinalizedDateMovement")
    samplerequiredenumdisplaytext = fields.Char(string="SampleRequiredEnumDisplayText")
    samplingprocesscode = fields.Char(string="SamplingProcessCode")
    weightfinalatdisplaytext = fields.Char(string="WeightFinalAtDisplayText")
    deliverybasisofdisplaytext = fields.Char(string="DeliveryBasisOfDisplayText")
    statusenum = fields.Char(string="StatusEnum")
    modifypersonid = fields.Char(string="ModifyPersonId")
    lastmodifydate = fields.Char(string="LastModifyDate")
    modifyperson = fields.Char(string="ModifyPerson")
    customerid = fields.Char(string="CustomerId")
    lockid = fields.Char(string="LockId")
    birecordcreationdate = fields.Char(string="BiRecordCreationDate")
    
    def import_nomination(self):
        interface = self.env['fusion.sync.history']
        last_sync = '2023-01-01'
        url = "https://fusionsqlmirrorapi.azure-api.net/api/nomination"
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
                    self.create_update_nomination('nomination', data)
                interface.update_sync_interface('nomination')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_nomination(self):
        interface = self.env['fusion.sync.history']
        last_sync = interface.get_last_sync('nomination')
        url = "https://fusionsqlmirrorapi.azure-api.net/api/nomination"
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
                    self.regular_update_nomination('nomination', data)
                interface.update_sync_interface('nomination')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def create_update_nomination(self, interface_type, data):
        if interface_type == 'nomination':
            exists = self.env['nomination.controller.bi'].search([('nominationcontrollerbiid', '=', data['nominationcontrollerbiid'])])
            if exists:
                return
                # if exists:
                #     return
                # else:
                #     self.env['cashflow.controller.bi'].search([('cashflowid', '=', data['cashflowid'])]).unlink()
                #     self.env['cashflow.controller.bi'].create(data)
                #     self.env.cr.commit()
            else:
                self.env['nomination.controller.bi'].create(data)
                self.env.cr.commit()
    
    def regular_update_nomination(self, interface_type, data):
        if interface_type == 'nomination':
            exists = self.env['nomination.controller.bi'].search([('nominationcontrollerbiid', '=', data['nominationcontrollerbiid'])])
            if exists:
                self.env['nomination.controller.bi'].search([('nominationcontrollerbiid', '=', data['nominationcontrollerbiid'])]).unlink()
                self.env['nomination.controller.bi'].create(data)
            else:
                self.env['nomination.controller.bi'].create(data)
                self.env.cr.commit()