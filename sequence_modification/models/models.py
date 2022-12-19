import datetime

from odoo import api, fields, models, _


class AccountMoveInheritModel(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # here we modify sequence on the base of date for both invoice and bill
        if self.move_type == 'out_invoice':
            self.generate_sequence('invoice.sequence')

        elif self.move_type == 'in_invoice':
            self.generate_sequence('bill.sequence')

        elif self.move_type == 'in_refund':
            self.generate_sequence('debit.sequence')

        elif self.move_type == 'out_refund':
            self.generate_sequence('credit.sequence')

        res = super().action_post()
        return res

    def generate_sequence(self, code=None):
        seq = self.env['ir.sequence'].next_by_code(code).split("-")
        short_name = str(self.partner_id.short_name) if self.partner_id.short_name else ''
        self.name = short_name + seq[0] + "-" + seq[
            1] + "-" + str(datetime.datetime.now().year)[
                       2:4] + "" + str(
            datetime.datetime.now().month)[:] + "" + seq[2]

    # this default function will change the sequence of credit note and debit note on clicking create button
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if res.get('move_type', '') == "out_refund":
            self.get_default_sequence(res, 'credit.sequence')

        elif res.get('move_type', '') == "in_refund":
            self.get_default_sequence(res, 'debit.sequence')

        elif res.get('move_type', '') == "out_invoice":
            self.get_default_sequence(res, 'invoice.sequence')

        elif res.get('move_type', '') == "in_invoice":
            self.get_default_sequence(res, 'bill.sequence')

        return res

    def get_default_sequence(self, res=None, code=None):
        seq = self.env['ir.sequence'].next_by_code(code).split("-")
        name = seq[0] + "-" + seq[1] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
            datetime.datetime.now().month)[:] + "" + seq[2]
        res['name'] = name


class DeliverySequenceInheritModel(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals_list):
        if self.env['stock.picking.type'].browse(vals_list.get('picking_type_id')).code == "outgoing":
            seq = self.env['ir.sequence'].next_by_code('delivery.sequence').split("-")
            short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
                'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
            name = short_name + seq[0] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
                datetime.datetime.now().month)[:] + str(
                datetime.datetime.now().day)[:] + "" + "-" + seq[1]
            vals_list['name'] = name
        res = super().create(vals_list)
        return res


class SaleOrderInheritModel(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals_list):
        seq = self.env['ir.sequence'].next_by_code('sale.order.sequence').split("-")
        short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
            'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
        name = short_name + seq[0] + "-" + seq[1] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
            datetime.datetime.now().month)[:] + "" + seq[2]
        vals_list['name'] = name
        vals_list['deal_ref'] = name.split('-')[0] + '-' + name.split('-')[2]
        res = super().create(vals_list)
        return res


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        sequence = self.env.ref('sequence_modification.payment_voucher_sequence_id')
        if sequence:
            sequence.write({
                'prefix': 'PV-' if self.payment_type == 'outbound' else "RV-"
            })
        seq = self.env['ir.sequence'].next_by_code('payment.voucher.sequence')
        self.name = seq
        res = super().action_post()
        return res
