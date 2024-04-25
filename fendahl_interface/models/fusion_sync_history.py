from odoo import models, fields, api
import requests
import logging
import datetime

_logger = logging.getLogger(__name__)
class FusionSyncHistory(models.Model):
    _name = 'fusion.sync.history'
    
    interface_type = fields.Char("Interface Type")
    last_sync = fields.Char("Interface Type")
    ##CASHFLOW
    
    ##NOMINATION
    def import_nomination(self):
        last_sync = self.get_last_sync('cashflow')
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
                json_data = self.lowercase_keys(json_data)
                for data in json_data:
                    self.create_update_cashflow('nomination', data)
                self.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_nomination(self):
        last_sync = self.get_last_sync('cashflow')
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
                json_data = self.lowercase_keys(json_data)
                for data in json_data:
                    self.regular_update_cashflow('cashflow', data)
                self.update_sync_interface('cashflow')
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def lowercase_keys(self,data):
        if isinstance(data, dict):
            return {k.lower(): self.lowercase_keys(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.lowercase_keys(item) for item in data]
        else:
            return data
    def get_last_sync(self, interface_type):
        interface_record = self.env['fusion.sync.history'].search([('interface_type', '=', interface_type)])
        if interface_record:
            return interface_record.last_sync
        else:
            return '2023-01-01'
    def update_sync_interface(self, interface_type):
        interface_record = self.env['fusion.sync.history'].search([('interface_type', '=', interface_type)])
        if interface_record:
            interface_record.last_sync = datetime.datetime.now()
        else:
            self.env['fusion.sync.history'].create(
                {
                    'interface_type': interface_type,
                    'last_sync': datetime.datetime.now()
                })
            
    
