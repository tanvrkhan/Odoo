# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from datetime import datetime,date, timedelta
from odoo.tools.misc import clean_context, OrderedSet, groupby

class RemarkSoldItem(models.TransientModel):
    _name = "change.module"
    _description = "Change Info"

    transfer_date = fields.Datetime(string="Transfer Date")
    remark = fields.Char(string="Remarks")

    def action_apply(self):
        order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        if not isinstance(self.transfer_date, datetime):
            raise UserError(_('Invalid transfer date.'))
        picking_id = self.env['stock.picking'].search([('sale_id', '=', order_id.id)], limit=1)
        if picking_id:
            if order_id.date_order >= self.transfer_date:
                raise UserError(_('You cannot force change the shipment date to a date backdated to the sale order. Please select a date after the Scheduled Sales order date.'))
        if self.transfer_date.date() >= datetime.now().date():
            raise UserError(_('Please Enter Correct Back Date'))
        active_model = self._context.get('active_model')
        picking_ids = False
        if active_model == 'sale.order':
            sale_order_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
            picking_list = [sale_id.picking_ids.ids for sale_id in sale_order_ids][0]
            picking_ids = self.env['stock.picking'].browse(picking_list)
        elif active_model == 'stock.picking':
            # if self._context.get
            picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids'))
        elif active_model == 'stock.picking.type':
            picking_type_id = self.env['stock.picking.type'].browse(self._context.get('active_id'))
            picking_ids = self.env['stock.picking'].search([('picking_type_id','=', picking_type_id.id),
                                                            ('state','!=','cancel')], order='id desc', limit=1)
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)
        
        pickings_without_moves = self.browse()
        pickings_without_quantities = OrderedSet()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
            
        if picking_ids:
            for picking in picking_ids.filtered(lambda x: x.state not in ('cancel')):
                for data in picking.move_ids_without_package:
                    data.write({'date': self.transfer_date, 'move_remark': self.remark, 'move_date': self.transfer_date})
                    for value in data.stock_valuation_layer_ids:
                        self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
                    for line in data.mapped('move_line_ids'):
                        line.write({'date': self.transfer_date or fields.Datetime.now(),'line_remark':self.remark})
                    for category in data.product_id.categ_id:
                      if category.property_valuation != 'real_time':
                            custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,
                                                                                'remarks':self.remark,
                                                                              'journal_id':data.product_id.categ_id.property_stock_journal.id,
                                                                              'ref':data.location_id.name,
                                                                              'stock_move_id':data.id})
            for transfer in picking_ids.filtered(lambda x: x.state not in ('done', 'cancel')):
                if not transfer.move_ids_without_package and not transfer.move_line_ids:
                    pickings_without_moves |= transfer
                for stock_move in transfer.move_ids_without_package:
                    print("-record",stock_move)
                    for account_move in stock_move.account_move_ids:
                         self.env.cr.execute(
                        "UPDATE account_move SET date = %s, remarks= %s WHERE id = %s",
                        [self.transfer_date, self.remark, account_move.id])
                transfer.message_subscribe([self.env.user.partner_id.id])
                picking_type = transfer.picking_type_id
                precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
                no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in transfer.move_line_ids)
                no_reserved_quantities = all(float_is_zero(move_line.reserved_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in transfer.move_line_ids)
                if no_reserved_quantities and no_quantities_done:
                    pickings_without_quantities |= picking.ids
                if picking_type.use_create_lots or picking_type.use_existing_lots:
                    lines_to_check = transfer.move_line_ids
                    if not no_quantities_done:
                        lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                        for line in lines_to_check:
                            product = line.product_id
                            if product and product.tracking != 'none':
                                if not line.lot_name and not line.lot_id:
                                    pickings_without_lots |= picking
                                    products_without_lots |= product

                if not transfer._should_show_transfers():
                    if pickings_without_moves:
                        raise UserError(_('Please add some items to move.'))
                    if pickings_without_quantities:
                        raise UserError(transfer._get_without_quantities_error_message())
                    if pickings_without_lots:
                        raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))         
                else:
                    message = ""
                    if pickings_without_moves:
                        message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
                    if pickings_without_quantities:
                        message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
                    if pickings_without_lots:
                        message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
                    if message:
                        raise UserError(message.lstrip())
                if not self.env.context.get('button_validate_picking_ids'):
                    transfer = transfer.with_context(button_validate_picking_ids=transfer.ids)
                res = transfer.with_context(from_custom=True,wiz_remark=self.remark,acc_date=self.transfer_date.date())._pre_action_done_hook()
                if res is not True:
                    return res
                if self.env.context.get('picking_ids_not_to_backorder'):
                    pickings_not_to_backorder = transfer.browse(self.env.context['picking_ids_not_to_backorder'])
                    pickings_to_backorder = transfer - pickings_not_to_backorder
                else:
                    pickings_not_to_backorder = self.env['stock.picking']
                    pickings_to_backorder = transfer
                    pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
                    pickings_to_backorder.with_context(cancel_backorder=False)._action_done()
            for stock_move in picking_ids.mapped('move_ids_without_package'):
                stock_move.stock_valuation_layer_ids._validate_accounting_entries()
        return True


    def skip_backdate(self):
        active_model = self._context.get('active_model')
        picking_ids = False
        if active_model == 'sale.order':
            sale_order_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
            picking_list = [sale_id.picking_ids.ids for sale_id in sale_order_ids][0]
            picking_ids = self.env['stock.picking'].browse(picking_list)
        elif active_model == 'stock.picking':
            picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids'))
        elif active_model == 'stock.picking.type':
            picking_type_id = self.env['stock.picking.type'].browse(self._context.get('active_id'))
            picking_ids = self.env['stock.picking'].search([('picking_type_id','=', picking_type_id.id),
                                        ('state','!=','cancel')], order='id desc', limit=1)
        return picking_ids.with_context(Skip=True).button_validate()       

class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'
    
    def process(self):
        if self._context.get('from_custom'):
            remark = self._context.get('wiz_remark') or ''
            date = self._context.get('acc_date') or fields.Date.today()
            result = super().process()
            picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids'))
            for stock_move in picking_ids.mapped('move_ids_without_package'):
                if stock_move.stock_valuation_layer_ids:
                    journal_entry_id = self.env['account.move'].search([('stock_move_id','=',stock_move.id)])
                    if not journal_entry_id:
                        self.create_journal_entry_forcely(stock_move.stock_valuation_layer_ids,remark,date)
            return result
        else:
            return super().process()
        
    def create_journal_entry_forcely(self,valuations,remark='',date=None):
        am_vals = []
        for svl in valuations:
            move = svl.stock_move_id
            if not move:
                move = svl.stock_valuation_layer_id.stock_move_id
            am_vals += move.with_company(svl.company_id)._account_entry_move(svl.quantity, svl.description, svl.id, svl.value)
        if am_vals:
            account_moves = self.env['account.move'].sudo().create(am_vals)
            if remark:
                account_moves.update({
                    'remarks':remark
                    })
            if date:
                account_moves.update({
                    'date':date
                    })
            account_moves._post()
        for svl in valuations:
            # Eventually reconcile together the invoice and valuation accounting entries on the stock interim accounts
            if svl.company_id.anglo_saxon_accounting:
                svl.stock_move_id._get_related_invoices()._stock_account_anglo_saxon_reconcile_valuation(product=svl.product_id)

class StockBackOrderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'
    
    
    
    