from odoo import models, fields, api
import requests
import logging
import datetime

_logger = logging.getLogger(__name__)


class FusionSyncHistoryErrors(models.Model):
    _name = 'fusion.sync.history.errors'
    
    interface_type = fields.Char("Interface Type")
    interface_id = fields.Char("Interface Id")
    error = fields.Text("Error")
    company= fields.Char("Internal Company")
    date = fields.Date("Date")
    
    def log_error(self, interface_type, interface_id, error,company):
        self.env['fusion.sync.history.errors'].create(
            {
                'interface_type': interface_type,
                'interface_id': interface_id,
                'error': error,
                'company': company,
                'date': datetime.datetime.now()
            })
class FusionSyncHistory(models.Model):
    _name = 'fusion.sync.history'
    
    interface_type = fields.Char("Interface Type")
    last_sync = fields.Char("Interface Type")
    
    ##CASHFLOW
    
    ##NOMINATION
    # def import_nomination(self):
    #     last_sync = self.get_last_sync('cashflow')
    #     url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
    #     headers = {
    #         'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
    #         'Content-Type': 'application/json',
    #     }
    #     params = {
    #         'date': last_sync
    #     }
    #     response = requests.get(url, headers=headers, params=params)
    #     if response.status_code == 200:
    #         try:
    #             json_data = response.json()
    #             json_data = self.lowercase_keys(json_data)
    #             for data in json_data:
    #                 self.create_update_cashflow('nomination', data)
    #             self.update_sync_interface('cashflow')
    #         except Exception as e:
    #             _logger.error('Error processing API data: %s', str(e))
    #     else:
    #         _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    # def sync_nomination(self):
    #     last_sync = self.get_last_sync('cashflow')
    #     url = "https://fusionsqlmirrorapi.azure-api.net/api/Cashflow"
    #     headers = {
    #         'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
    #         'Content-Type': 'application/json',
    #     }
    #     params = {
    #         'date': last_sync
    #     }
    #     response = requests.get(url, headers=headers, params=params)
    #     if response.status_code == 200:
    #         try:
    #             json_data = response.json()
    #             json_data = self.lowercase_keys(json_data)
    #             for data in json_data:
    #                 self.regular_update_cashflow('cashflow', data)
    #             self.update_sync_interface('cashflow')
    #         except Exception as e:
    #             _logger.error('Error processing API data: %s', str(e))
    #     else:
    #         _logger.error('Failed to fetch data from external API: %s', response.status_code)
    
    def sync_all(self):
        self.env['nomination.controller.bi'].sync_nomination()
        self.env['transfer.controller.bi'].sync_transfer()
        self.env['cashflow.controller.bi'].sync_cashflow()
        self.env['trade.controller.bi'].sync_trade()
        self.env['invoice.controller.bi'].sync_invoice()
    def get_partner_info(self,info):
        result =''
        url = "https://fusionsqlmirrorapi.azure-api.net/api/partner"
        headers = {
            'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
            'Content-Type': 'application/json',
        }
        params = {
            'code': info
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                result = response.json()
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        return result
    
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
    def validate_product(self, commodity,name,uom):
        product = self.env['product.template'].search([('name', '=', name)], limit=1)
        if not product:
            category=''
            if commodity=='Coal':
                category = 4
            elif commodity=="Pellets" or commodity =="Pellets Industrial":
                category = 27
            elif commodity=="Refined Products":
                category = 28
                
            product = self.env['product.template'].create({
                'name': name,
                'type': 'product',
                'categ_id': category,
                'uom_id': 1,
                'default_code': 'Fusion - Do not use directly'
            })
            uom = self.validate_uom(product,uom)
            product.uom_id= uom.id
            product.uom_po_id = uom.id
        
        if product:
            product= self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1)
        return product
    def validate_uom(self,product,uomname):
        if uomname:
            result = self.env['uom.uom'].search(
            [('category_id', '=', product.uom_id.category_id.id), ('name', '=', uomname)])
        
            if not result:
                conversionfactor=1
                uom_type='reference'
                if uomname=='MT':
                    conversionfactor=1
                    uom_type='reference'
                else:
                    conversionfactor = self.get_uom_conversion_factor(product,'MT',uomname)
                    if conversionfactor:
                        if conversionfactor<1:
                            uom_type='smaller'
                        else:
                            uom_type='bigger'
                    else:
                        conversionfactor =1
                result = self.env['uom.uom'].create({
                    'name': uomname,
                    'category_id': product.uom_id.category_id.id,
                    'ratio': conversionfactor,
                    'uom_type': uom_type
                })
            return result
        else:
            return
    def get_uom_conversion_factor(self,product,fromuom,touom):
        result = ''
        url = "https://fusionsqlmirrorapi.azure-api.net/api/uom"
        headers = {
            'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
            'Content-Type': 'application/json',
        }
        params = {
            'product': product,
            'fromuom': fromuom,
            'touom': touom
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                result = response.json()
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        return result
    
    def validate_warehouse(self,warehouse,company):
        result = self.env['stock.warehouse'].search([('name', '=', warehouse),('company_id', '=', company)], limit=1)
        if not result:
            result = self.env['stock.warehouse'].create({
                'name': warehouse,
                'code':warehouse,
                'company_id': company,
                'partner_id':company
            })
        return result
            
    def checkAndDefineAnalytic(self, planName, account,company):
        analytic_plan = self.env['account.analytic.plan'].search([('name', '=', planName),
                                                                  ('company_id', '=', company)])
        if not (analytic_plan):
            analytic_plan = self.env['account.analytic.plan'].create({
                'name': planName,
                'company_id': company
            })
        analytic_account = self.env['account.analytic.account'].search([('name', '=', account),
                                                                       ('plan_id', '=', analytic_plan.id),
                                                                        ('company_id', '=', company)])
        if not analytic_account:
            analytic_account = self.env['account.analytic.account'].create(
                {'name': account,
                 'plan_id': analytic_plan.id,
                 'company_id': company
                 })
        return analytic_account
    def validate_lot(self,name,product,company):
        lot = self.env['stock.lot'].search([('name', '=', name),('product_id', '=', product),('company_id', '=', company)], limit=1)
        if not lot:
            lot = self.env['stock.lot'].create({
            'name': name,
            'product_id': product,
            'company_id': company,
        })
        return lot
        
            
            
            
        
        
    
