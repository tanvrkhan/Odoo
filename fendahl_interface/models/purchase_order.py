import datetime
import json
import requests
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, datetime
from odoo.exceptions import ValidationError


class PurchaseOrderSync(models.Model):
    _inherit = 'purchase.order'
    fusion_deal_number = fields.Char('Deal')
    
                    
            
            
            

class PurchaseOrderLineSync(models.Model):
    _inherit = 'purchase.order.line'
    
    fusion_segment_id = fields.Integer('Fusion Trade section')