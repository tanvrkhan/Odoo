# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class InheritStockMoveLine(models.Model):
	_inherit = 'stock.move.line'
	
	def fix_incoming_outgoing_locations(self):
		for record in self:
			lots = record.lot_id
			for lot in lots:
				deliveries_to_fix = []
				correct_deliveries = []
				deliveries_of_lot = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
				for deliveries in deliveries_of_lot:
					if (deliveries.location_id.id == 8 or deliveries.location_dest_id.id == 8):
						deliveries_to_fix.append(deliveries)
					else:
						correct_deliveries.append(deliveries)
				
				# correct_deliveries = lot.delivery_ids.search(
				# 	['|', '&', ('location_id.id', '!=', 8), ('location_dest_id.id', '!=', 8),
				# 	 ('id', 'in', lot.delivery_ids.id)])
				if (deliveries_to_fix) and correct_deliveries:
					for entry in correct_deliveries:
						correct_location = 0
						# correct_location = correct_deliveries.search([('location_id.usage', '=', 'internal')])
						if entry.location_id.usage == 'internal':
							correct_location = entry.location_id
						if entry.location_dest_id.usage == 'internal':
							correct_location = entry.location_dest_id
						if correct_location != 0 and len(deliveries_to_fix) > 0:
							for dtf in deliveries_to_fix:
								if dtf.location_id.id == 8:
									dtf.location_id = correct_location
									dtf.move_id.location_id = correct_location
									dtf.move_id.picking_id.location_id = correct_location
								elif dtf.location_dest_id.id == 8:
									dtf.location_dest_id = correct_location
									dtf.move_id.location_dest_id = correct_location
									dtf.move_id.picking_id.location_dest_id = correct_location
# @api.onchange('lot_id_custom')
# def _update_child_lots(self):
#     for rec in self:
#         for line in rec.move_line_ids:
#             line.update({'lot_id': [(4, rec.lot_id_custom.id)]})
#
#         # for line in rec.move_line_ids:
#         #     if line.product_id == self.product_id:
#         #         # line.write({'lot_id':self.lot_id_custom.id})
