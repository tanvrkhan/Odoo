import datetime

from odoo import api, fields, models, _


class AccountMoveInheritModel(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.move_type == 'out_invoice':
            self.generate_sequence('invoice.sequence', 'invoice')

        elif self.move_type == 'in_invoice':
            self.generate_sequence('bill.sequence', 'bill')

        elif self.move_type == 'in_refund':
            self.generate_sequence('debit.sequence', 'refund')

        elif self.move_type == 'out_refund':
            self.generate_sequence('credit.sequence', 'credit')

        elif self.move_type == 'entry':
            seq = self.env['ir.sequence'].next_by_code('journal.entry.sequence')
            self.name = seq

        res = super().action_post()
        return res

    def generate_sequence(self, code=None, move_type=None):
        seq = self.env['ir.sequence'].next_by_code(code).split("-")
        next_num = 0
        if seq:
            if move_type == "invoice":
                self.partner_id.inv_partner_seq += 1
                next_num = self.partner_id.inv_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
            elif move_type == "bill":
                self.partner_id.bill_partner_seq += 1
                next_num = self.partner_id.bill_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
            elif move_type == "refund":
                self.partner_id.refund_partner_seq += 1
                next_num = self.partner_id.refund_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
            elif move_type == "credit":
                self.partner_id.credit_partner_seq += 1
                next_num = self.partner_id.credit_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
            else:
                self.partner_id.refund_partner_seq += 1
                next_num = self.partner_id.refund_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name

    def get_new_name(self, seq=None, next_num=None):
        month = self.get_month()
        short_name = str(self.partner_id.short_name) if self.partner_id.short_name else ''
        if next_num in list(range(10)):
            name = short_name + seq[0] + "-" + seq[
                1] + "-" + str(datetime.datetime.now().year)[
                           2:4] + "" + str(month) + "" + "0" + str(next_num)
        else:
            name = short_name + seq[0] + "-" + seq[
                1] + "-" + str(datetime.datetime.now().year)[
                           2:4] + "" + str(month) + "" + str(next_num)

        return name

    @staticmethod
    def get_month():
        month = datetime.datetime.now().month
        if month in list(range(10)):
            return "0" + str(month)
        return month

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
        month = self.get_month()
        seq = self.env['ir.sequence'].next_by_code(code).split("-")
        name = seq[0] + "-" + seq[1] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(month) + "" + seq[2]
        res['name'] = name


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals_list):
        if self.env['stock.picking.type'].browse(vals_list.get('picking_type_id')).code == "outgoing":
            self.create_seq_name(vals_list)
        res = super().create(vals_list)
        return res

    @staticmethod
    def get_month():
        month = datetime.datetime.now().month
        if month in list(range(10)):
            return "0" + str(month)
        return month

    def create_seq_name(self, vals_list=None):
        seq = self.env['ir.sequence'].next_by_code('delivery.sequence').split("-")
        next_num = 0
        short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
            'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
        if seq:
            partner = self.env['res.partner'].browse(vals_list.get('partner_id'))
            partner.picking_partner_seq += 1
            next_num = partner.picking_partner_seq
            name = self.get_new_name(seq, next_num, short_name)
            is_exist = self.env['stock.picking'].search([('name', '=', name)])
            if is_exist:
                self.create_seq_name(vals_list)
            else:
                vals_list['name'] = name

    def get_new_name(self, seq=None, next_num=None, short_name=None):
        month = self.get_month()
        if next_num in list(range(10)):
            name = short_name + seq[0] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
                month) + "0" + str(next_num)
        else:
            name = short_name + seq[0] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
                month) + str(next_num)
        return name


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals_list):
        self.sale_create_seq_name(vals_list)
        res = super().create(vals_list)
        return res

    @staticmethod
    def get_month():
        month = datetime.datetime.now().month
        if month in list(range(10)):
            return "0" + str(month)
        return month

    def sale_create_seq_name(self, vals_list=None):
        seq = self.env['ir.sequence'].next_by_code('sale.order.sequence').split("-")
        next_num = 0
        short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
            'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
        if seq:
            partner = self.env['res.partner'].browse(vals_list.get('partner_id'))
            partner.so_partner_seq += 1
            next_num = partner.so_partner_seq
            name = self.get_new_name(seq, next_num, short_name)
            is_exist = self.env['sale.order'].search([('name', '=', name)])
            if is_exist:
                self.sale_create_seq_name(vals_list)
            else:
                vals_list['name'] = name
                vals_list['deal_ref'] = name.split("-")[0] + "-" + name.split("-")[2]
                return vals_list

    def get_new_name(self, seq=None, next_num=None, short_name=None):
        month = self.get_month()
        if next_num in list(range(10)):
            name = short_name + seq[0] + "-" + seq[1] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
                month) + "" + "0" + str(next_num)
        else:
            name = short_name + seq[0] + "-" + seq[1] + "-" + str(datetime.datetime.now().year)[2:4] + "" + str(
                month) + "" + str(next_num)
        return name


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    pv_count = fields.Float("Pv Count")
    rv_count = fields.Float("Pv Count")

    def action_post(self):
        self.generate_payment_sequence()
        res = super().action_post()
        return res

    def generate_payment_sequence(self):
        if self.payment_type != 'outbound':
            seq = self.env['ir.sequence'].next_by_code('payment.receive.sequence')
            check_name = self.check_exist(seq)
            if check_name:
                self.generate_payment_sequence()
            else:
                self.name = seq
        else:
            seq = self.env['ir.sequence'].next_by_code('payment.voucher.sequence')
            check_name = self.check_exist(seq)
            if check_name:
                self.generate_payment_sequence()
            else:
                self.name = seq

    def check_exist(self, seq=None):
        return self.env['account.payment'].search([('name', '=', seq)])


class InheritResCustomer(models.Model):
    _inherit = 'res.partner'

    inv_partner_seq = fields.Integer("Invoice Sequence")
    bill_partner_seq = fields.Integer("Bill Sequence")
    credit_partner_seq = fields.Integer("Credit Note Sequence")
    refund_partner_seq = fields.Integer("Refund Sequence")
    picking_partner_seq = fields.Integer("Picking Sequence")
    so_partner_seq = fields.Integer("SO Sequence")
