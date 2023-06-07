# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class StockLot(models.Model):
    _inherit="stock.lot"

    def name_get(self):
        return [(lot.id, lot.name+ " "+ str(lot.product_qty) + " "+ str(lot.product_id.uom_id.name) ) for lot in self]