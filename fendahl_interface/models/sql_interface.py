# import datetime
# import json
# import requests
# # import pymssql
# from odoo import api, fields, models, _
# from dateutil import parser
# from datetime import date, datetime
# from odoo.exceptions import ValidationError
# import pyodbc
#
#
# class PurchaseOrderFusion(models.Model):
#     _inherit = 'purchase.order'
#     deal_master_id= fields.Integer("Deal Master")
#     segment_id= fields.Integer("Segment")
#     load_location_fusion = fields.Text("Load Location")
#     discharge_location_fusion = fields.Text("Discharge Location")
#
#     def sql_purchase_orders_import(self):
#         cnxn =  pyodbc.connect(server='mis.ukwest.cloudapp.azure.com,1499', user='fusionkemexonbi', password='fu$ion@123', database='fusion_kemexon_prod_mirror')
#
#         cursor = cnxn.cursor()
#         for row in cursor.execute("select top 1 * from Trade_controller_BI"):
#             if row.Buy_Sell=='Buy':
#                 deal = self.env['purchase.order'].search(['deal_master_id','=',row.Deal_Master_Id])
#                 if deal:
#                     #Check segment
#                     segment = self.env['purchase.order'].search(['deal_master_id','=',row.Deal_Master_Id],['segment_id','=',row.Segment_Id])
#                     if segment:
#                         raise ValidationError("Line already exists")
#                         #update segment
#                     else:
#                         raise ValidationError("Order exists but Line doesn't exist")
#                         #Create segment
#                 else:
#                     partner = self.env['res.partner'].search(['name', '=', row.CounterPart_Company]).id
#                     product = self.env['product.template'].search(['name', '=', row.Material])
#                     currency = self.env['res.currency'].search(['name', '=', row.Settlement_Currency]).id
#                     company=0
#
#
#                     if row.InternalCompany=='KEMEXON LTD':
#                         company=1
#                     elif row.InternalCompany =='KEMEXON SA':
#                         company=2
#                     elif row.InternalCompany == 'Kemexon BELGIUM SRL':
#                         company=3
#                     elif row.InternalCompany == 'RUVUMA COAL LIMITED':
#                         if row.CounterPart_Company == 'KEMEXON LTD':
#                             company = 1
#                             partner = self.env['res.partner'].search(['name', '=', row.InternalCompany]).id
#                         elif row.CounterPart_Company == 'KEMEXON SA':
#                             company = 2
#                             partner = self.env['res.partner'].search(['name', '=', row.InternalCompany]).id
#                         elif row.CounterPart_Company == 'Kemexon BELGIUM SRL':
#                             company = 3
#                             partner = self.env['res.partner'].search(['name', '=', row.InternalCompany]).id
#
#                     commodity_ann = self.checkAndDefineAnalytic('Commodity', row.Commodity)
#                     trader_ann= self.checkAndDefineAnalytic('Trader', row.Trader_Person)
#                     strategy_ann= self.checkAndDefineAnalytic('Strategy', row.Strategy)
#                     businessunit_ann = self.checkAndDefineAnalytic('Business Unit', row.Business_Unit)
#
#
#                     if not partner:
#                         raise ValidationError("Partner doesn't exist.")
#                     if not product:
#                         raise ValidationError("Product doesn't exist.")
#                     else:
#                         order= self.env['purchase_order'].create({
#                             'partner_id': partner,  # Example supplier's ID
#                             'date_order': row.Trade_Date,  # Example order date
#                             'partner_ref': row.External_Ref,  # Example supplier's ID
#                             'currency_id': currency,
#                             'load_location_fusion ' : row.Load_Location,
#                             'discharge_location_fusion ': row.Discharge_Location,
#                             'incoterm_id': row.Delivery_Term,
#                             'order_line' : [(0, 0, {
#                             'name': product,
#                             'product_id': product,
#                             'product_qty': row.Trade_Qty if row.Trade_Qty>0 else row.Trade_Qty*-1,
#                             'price_unit': row.Trade_Price if isinstance(row.Trade_Price, (int, float)) else 0,
#                             'date_planned': row.Trade_Date,
#                                 'analytic_distribution':{
#                                     commodity_ann:100,
#                                     trader_ann:100,
#                                     strategy_ann:100,
#                                     businessunit_ann:100
#                                 }
#                             # 'product_uom': product['uom_id'],
#                         })]
#                         })
#
#                     #Check Masters and create deal
#                     #Create new deal
#             #
#             # else:
#             #     #Sell code here
#             #
#             #
#             #
#             #
#             # # Dynamically generate order lines from the products list
#             #
#             #
#             #     order_lines.append(line)
#             #
#             # order_vals['order_line'] = order_lines
#             #
#             # print row.bla, row.anotherbla
#     def checkAndDefineAnalytic(self,planName,account):
#         analytic_plan = self.env['account.analytic.plan'].search(['name', '=', planName],['company_id','=',self.company_id])
#         if not (analytic_plan):
#             analytic_plan = self.env['account.analytic.plan'].create({
#                 'name': planName,
#                 'company_id':  self.company_id
#             })
#         analytic_account = self.env['account.analytic.account'].search(['name', '=', account],
#                                                                 ['plan_id', '=', analytic_plan.id],
#                                                                 ['company_id', '=', self.company_id])
#         if not analytic_account:
#             analytic_account = self.env['account.analytic.account'].create(
#                 {'name': account,
#                  'plan_id': analytic_plan.id,
#                  'company_id' : self.company_id
#                  })
#         return analytic_account