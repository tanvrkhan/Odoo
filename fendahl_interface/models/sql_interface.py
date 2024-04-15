# import datetime
# import json
# import requests
# import pyodbc
# from odoo import api, fields, models, _
# from dateutil import parser
# from datetime import date, datetime
# from odoo.exceptions import ValidationError
#
#
# class AccountMoveFusion(models.Model):
#     _inherit = 'account.move'
#
#
#
#
#     def get_rows_process(self):
#         cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                               "Server=mis.ukwest.cloudapp.azure.com\REPLICA,1499;"
#                               "Database=fusion_kemexon_prod_mirror;"
#                               "uid=fusionkemexonbi;pwd=fu$ion@123;"
#                               "Trusted_Connection=yes;")
#         cursor = cnxn.cursor()
#         for row in cursor.execute("select bla, anotherbla from blabla"):
#             print row.bla, row.anotherbla