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
    
    def validate_cost(self,  name):
        product = self.env['product.template'].search([('name', '=', name)], limit=1)
        if not product:
            product = self.env['product.template'].create({
                'name': name,
                'type': 'service',
                'categ_id': 14,
                'uom_id': 1,
                'default_code': 'Fusion - Do not use directly',
                'invoice_policy': 'order'
            })
        if product:
            product = self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1)
        return product
    
    
    def validate_product(self, commodity,name,uom):
        product = self.env['product.template'].search([('id', '=', 0)], limit=1)
        category=0
        if commodity=='Coal':
            category = 4
            product = self.env['product.template'].search([('name', '=', name)],
                                                          limit=1)
        elif commodity=="Pellets" or commodity =="Pellets Industrial":
            category = 27
            product = self.env['product.template'].search([('name', '=', name)],
                                                          limit=1)
        elif commodity=="Refined Products":
            category = 28
            product = self.env['product.template'].search([('name', '=', name), ('default_code', '=', 'I')],
                                                          limit=1)
        if not product:
            product = self.env['product.template'].create({
                'name': name,
                'type': 'product',
                'categ_id': category,
                'uom_id': 1,
                'default_code': 'I',
                'invoice_policy': 'delivery'
            })
            category_type= 'liquids' if  commodity=="Refined Products" else 'solids'
            uom = self.create_new_product_uom(product,uom,category_type)
            product.uom_id= uom.id
            product.uom_po_id = uom.id
        
        if product:
            product= self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1)
        return product
    
    def create_new_product_uom(self, product, uomname,category_type):
        if uomname:
            uom_type=''
            base_unit = self.get_base_unit(product.name)
            result = self.env['uom.uom']
            if category_type=='solids':
                category = self.env['uom.category'].search([('name', '=', 'solids')], limit=1)
                if not category:
                    category = self.env['uom.category'].create({
                        'name': 'Solids'
                    })
            else:
                category = self.env['uom.category'].search([('name', '=', product.name)], limit=1)
                if not category:
                    category = self.env['uom.category'].create({
                        'name': product.name
                    })
                    reference_uom = self.env['uom.uom'].create({
                        'name': base_unit,
                        'category_id': category.id,
                        'ratio': 1,
                        'uom_type': 'reference'
                    })
            result = self.env['uom.uom'].search(
                [('category_id', '=', category.id), ('name', '=', uomname)])
            
            if not result:
                uom_category = category
                conversionfactor = 1
            # reference_uom = self.env['uom.uom'].search([('category_id', '=', category.id),('uom_type', '=', 'reference')], limit=1)
                if base_unit==uomname:
                    conversionfactor = 1
                    uom_type = 'reference'
                else:
                    conversionfactor = self.get_uom_conversion_factor(product, base_unit, uomname)
                    if float(conversionfactor) < 1:
                        uom_type = 'bigger'
                    else:
                        uom_type = 'smaller'
                result = self.env['uom.uom'].create({
                    'name': uomname,
                    'category_id': category.id,
                    'ratio': conversionfactor,
                    'uom_type': uom_type  if uom_type else 'bigger'
                })
            return result

    
    def validate_uom(self,product,uomname):
        if uomname:
            base_unit = self.get_base_unit(product.name)
            # if base_unit==uomname:
            #     return self.env['uom.uom'].search(
            #     [('category_id', '=', product.uom_id.category_id.id), ('name', '=', uomname)])
            # else:
            result = self.env['uom.uom'].search(
            [('category_id', '=', product.uom_id.category_id.id), ('name', '=', uomname)])
            if not result:
                uom_category = self.env['uom.category'].search(
                    [('id', '=', product.uom_id.category_id.id)])
                if uomname==base_unit:
                    conversionfactor = 1
                    uom_type = 'reference'
                else:
                    conversionfactor = self.get_uom_conversion_factor(product,base_unit,uomname)
                    if conversionfactor:
                        if float(conversionfactor)<1:
                            uom_type='bigger'
                        else:
                            uom_type='smaller'
                    else:
                        conversionfactor =1
                result = self.env['uom.uom'].create({
                    'name': uomname,
                    'category_id': product.uom_id.category_id.id,
                    'ratio': conversionfactor,
                    'uom_type': uom_type,
                    'rounding':0.001
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
            'product': product.name,
            'fromuom': fromuom,
            'touom': touom
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                result = response.json()
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        else:
            params = {
                'product': product.name,
                'fromuom': fromuom,
                'touom': touom
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception as e:
                    _logger.error('Error processing API data: %s', str(e))
            else:
                if fromuom=='MT' and touom=='MT (Vac)':
                    conversionfactor = 0.998
                elif fromuom=='MT (Vac)' and touom=='MT':
                    conversionfactor = 1.002
                else:
                    conversionfactor = 1
                result = conversionfactor
        return result
    
    def get_base_unit(self,material):
        result = ''
        url = "https://fusionsqlmirrorapi.azure-api.net/api/ProductBaseUnit"
        headers = {
            'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
            'Content-Type': 'application/json',
        }
        params = {
            'material': material,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                result = response.text
            except Exception as e:
                _logger.error('Error processing API data: %s', str(e))
        return result
    
    
    def get_wh_code(self,warehouse,company,iteration):
        code=''
        warehouse=warehouse.replace(' ','')
        if len(warehouse)<iteration+5:
            code=warehouse
        else:
            code = warehouse[iteration:iteration+5]
        existing_warehouse = self.env['stock.warehouse'].search([('code', '=', code), ('company_id', '=', company)])
        if existing_warehouse:
            iteration+=1
            code = self.get_wh_code(warehouse,company,iteration)
            return code
        else:
            return code
            
    def validate_warehouse(self,warehouse,company,nomkey):
        result = self.env['stock.warehouse'].search([('name', '=', nomkey),('company_id', '=', company)], limit=1)
        
        if not result:
            code = self.get_wh_code(warehouse, company, 0)
            result = self.env['stock.warehouse'].create({
                'name': nomkey,
                'code':code,
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
    
    def get_tax_record(self, code,purchasesale,company):
        if code:
            result = self.env['account.tax']
            url = "https://fusionsqlmirrorapi.azure-api.net/api/TaxRate"
            headers = {
                'Ocp-Apim-Subscription-Key': '38cb5797102f4b1f852ae8ff6e8482e5',
                'Content-Type': 'application/json',
            }
            params = {
                'ratecode': code,
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                try:
                    result_json = response.json()
                    result_pct = result_json['percentageRate']
                    name = result_json['taxRateCode']
                    currency = result_json['currencyCode']
                    
                    result =  self.env['account.tax'].search([('name','=',name),('type_tax_use', '=', purchasesale),('company_id', '=', company)], limit=1)
                    if not result:
                        new_tax = self.env['account.tax'].create({
                            'name': name,
                            'amount': result_pct,  # Tax percentage rate
                            'amount_type': 'percent',  # 'percent' for percentage or 'fixed' for fixed amount
                            'description': purchasesale.capitalize() +' ' + str(result_pct),
                            'type_tax_use': purchasesale,  # 'sale' for sales, 'purchase' for purchases, or 'none' for none
                            'price_include': False,  # True if the tax is included in the price
                            'include_base_amount': False,  # True if tax affects the base amount for subsequent taxes
                            'sequence': 10,  # Determines the order of the tax application
                            'company_id': company,
                        })
                        
                except Exception as e:
                    _logger.error('Error processing API data: %s', str(e))
            return result
        else:
            return
            
            
        
        
    
