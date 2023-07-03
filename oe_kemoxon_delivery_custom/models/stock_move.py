# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class InheritStockMove(models.Model):
	_inherit = 'stock.move'
	
	lot_id_custom = fields.Many2one('stock.lot', string='Primary Lot', domain="[('product_id', '=', product_id)]")

# @api.onchange('lot_id_custom')
# def _update_child_lots(self):
#     for rec in self:
#         for line in rec.move_line_ids:
#             line.update({'lot_id': [(4, rec.lot_id_custom.id)]})
#
#         # for line in rec.move_line_ids:
#         #     if line.product_id == self.product_id:
#         #         # line.write({'lot_id':self.lot_id_custom.id})
