import datetime
from odoo import api, fields, models, _
from dateutil import parser
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class AccountMoveInheritModel(models.Model):
    _inherit = 'account.move'

    move_sequence_done = fields.Boolean("Sequence Done")

    def action_post(self):
        for rec in self:
            if not rec.move_sequence_done and rec.name == '/':
                if rec.move_type == 'out_invoice' and ((rec.journal_id.id == 2  and rec.company_id.id==1) or(rec.journal_id.id == 36  and rec.company_id.id==2)):
                    rec.generate_sequence('invoice.sequence', 'invoice')

                elif rec.move_type == 'out_invoice' and ((rec.journal_id.id != 2  and rec.company_id.id==1) or(rec.journal_id.id != 36  and rec.company_id.id==2)):
                    rec.generate_sequence('invoice.provisional.sequence', 'invoice')

                elif rec.move_type == 'in_invoice' and ((rec.journal_id.id == 3  and rec.company_id.id==1) or(rec.journal_id.id == 37  and rec.company_id.id==2)):
                    rec.generate_sequence('bill.sequence', 'bill')

                elif rec.move_type == 'in_invoice' and ((rec.journal_id.id != 3  and rec.company_id.id==1) or(rec.journal_id.id != 37  and rec.company_id.id==2)):
                    rec.generate_sequence('bill.provisional.sequence', 'bill')
                
                elif rec.move_type == 'out_invoice' and rec.company_id!=1 and rec.company_id!=2:
                    rec.generate_sequence('invoice.sequence', 'invoice')
                    
                elif rec.move_type == 'in_invoice' and rec.company_id!=1 and rec.company_id!=2:
                    rec.generate_sequence('bill.sequence', 'invoice')

                elif rec.move_type == 'in_refund':
                    rec.generate_sequence('debit.sequence', 'refund')

                elif rec.move_type == 'out_refund':
                    rec.generate_sequence('credit.sequence', 'credit')

                # elif rec.move_type == 'entry':
                #     if not rec.move_sequence_done and rec.name == '/':
                #         rec.set_entry_seq()
        return super().action_post()
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.move_sequence_done=False
        default = dict(default or {})
        if (fields.Date.to_date(default.get('date')) or self.date) <= self.company_id._get_user_fiscal_lock_date():
            default['date'] = self.company_id._get_user_fiscal_lock_date() + timedelta(days=1)
        if self.move_type == 'entry':
            default['partner_id'] = False
        copied_am = super().copy(default)
        message_origin = '' if not copied_am.auto_post_origin_id else \
            '<br/>' + _('This recurring entry originated from %s', copied_am.auto_post_origin_id._get_html_link())
        copied_am._message_log(body=_(
            'This entry has been duplicated from %s%s',
            self._get_html_link(),
            message_origin,
        ))
        
        return copied_am
    def is_entry_sequence_exits(self, seq=None):
        seq = self.env['account.move'].search([('name', '=', seq)])
        if seq:
            return True
        else:
            return False

    # def set_entry_seq(self):
    #     seq = self.env['ir.sequence'].next_by_code('journal.entry.sequence')
    #     is_exists = self.is_entry_sequence_exits(seq)
    #     if is_exists:
    #         self.set_entry_seq()
    #     else:
    #         self.name = seq
    #         self.move_sequence_done = True

    def generate_sequence(self, code=None, move_type=None):
        seq = self.env['ir.sequence'].next_by_code(code).split("-")
        next_num = 0
        if seq:
            if move_type == "invoice" and code == 'invoice.sequence':
                self.partner_id.inv_partner_seq += 1
                next_num = self.partner_id.inv_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
                    if self.company_id.id != 4:
                        self.payment_reference = name
            elif move_type == "invoice" and code == 'invoice.provisional.sequence':
                self.partner_id.inv_prov_partner_seq += 1
                next_num = self.partner_id.inv_prov_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name
                    if self.company_id.id != 4:
                        self.payment_reference = name
            elif move_type == "bill" and code == 'bill.sequence':
                self.partner_id.bill_partner_seq += 1
                next_num = self.partner_id.bill_partner_seq
                name = self.get_new_name(seq, next_num)
                is_exists = self.env['account.move'].search([('name', '=', name)])
                if is_exists:
                    self.generate_sequence(code, move_type)
                else:
                    self.name = name

            elif move_type == "bill" and code == 'bill.provisional.sequence':
                self.partner_id.bill_prov_partner_seq += 1
                next_num = self.partner_id.bill_prov_partner_seq
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

        self.move_sequence_done = True

    def get_new_name(self, seq=None, next_num=None):
        month = self.get_month()
        year = self.get_year()
        short_name = str(self.partner_id.short_name) if self.partner_id.short_name else ''
        name = short_name + "-" + seq[1] + "-" + str(year) + "" + str(month)
        get_name = self.check_in_partner_seq(name)
        return get_name

    def get_year(self):
        year = str(datetime.datetime.now().year)[2:4]
        year = str(self.invoice_date.year)[-2:] if self.invoice_date else year
        return year

    def get_month(self):
        month = datetime.datetime.now().month
        if self:
            month = self.invoice_date.month if self.invoice_date else '0' + str(month) if month < 10 else str(month)
            if month in list(range(10)):
                return "0" + str(month)
            return month
        return None

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
        res['name'] = '/'

    def check_in_partner_seq(self, name=None):
        partner_seq_obj = self.env['partner.sequence']
        is_exists = partner_seq_obj.search([('name', '=', name), ('company_id', '=', self.env.company.id)])
        if is_exists:
            is_exists.next_number += 1
            new_name = is_exists.name + str(is_exists.next_number).zfill(3)
            return new_name
        else:
            is_kem_seq = partner_seq_obj.search([('name', '=', name), ('company_id', '=', False)])
            if is_kem_seq and self.env.company.id == 1:
                is_kem_seq.next_number += 1
                new_name = is_kem_seq.name + str(is_kem_seq.next_number).zfill(3)
                return new_name
            else:
                num = 1
                # new_name = name + str(num).zfill(3)
                new_name = name + str(num).zfill(3)
                num += 1
                partner_seq_obj.create({
                    'name': name,
                    'next_number': num,
                    'company_id': self.env.company.id
                })
                return new_name


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    deal_ref = fields.Char("Deal Ref")

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.origin:
            if self.env['stock.picking.type'].browse(vals_list.get('picking_type_id')).code == "outgoing":
                name = self.create_seq_name(vals_list, rec=res)
                res.name = name
        return res

    @staticmethod
    def get_month():
        month = datetime.datetime.now().month
        if month in list(range(10)):
            return "0" + str(month)
        return month

    def create_seq_name(self, vals_list=None, rec=None):
        seq = self.env['ir.sequence'].next_by_code('delivery.sequence').split("-")
        next_num = 0
        short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
            'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
        if seq:
            partner = self.env['res.partner'].browse(vals_list.get('partner_id'))
            partner.picking_partner_seq += 1
            next_num = partner.picking_partner_seq
            name = self.get_new_name(seq, next_num, short_name, rec)
            is_exist = self.env['stock.picking'].search([('name', '=', name)])
            if is_exist:
                self.create_seq_name(vals_list, rec)
            else:
                vals_list['name'] = name
                return name

    def get_new_name(self, seq=None, next_num=None, short_name=None, rec=None):
        if rec.origin:
            origin = "-".join(rec.origin.split('-')[0::2])
            new_name = self.check_in_partner_seq(origin)
            return new_name
        else:
            origin = rec.name
        name = origin + "-" + str(seq[1])
        return name

    def check_in_partner_seq(self, name=None):
        partner_seq_obj = self.env['partner.sequence']
        is_exists = partner_seq_obj.search([('name', '=', name), ('company_id', '=', self.env.company.id)])
        if is_exists:
            new_name = is_exists.name + '-' + str(is_exists.next_number).zfill(3)
            is_exists.next_number += 1
            return new_name
        else:
            is_kem_seq = partner_seq_obj.search([('name', '=', name), ('company_id', '=', False)])
            if is_kem_seq and self.env.company.id == 1:
                is_kem_seq.next_number += 1
                new_name = is_kem_seq.name + '-' + str(is_kem_seq.next_number).zfill(3)
                return new_name
            else:
                num = 1
                new_name = name + '-' + str(num).zfill(3)
                num += 1
                partner_seq_obj.create({
                    'name': name,
                    'next_number': num,
                    'company_id': self.env.company.id
                })
                return new_name


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    hidden_ref = fields.Char("Hidden Ref", copy=False)
    deal_ref = fields.Char("Deal Ref", copy=False)

    @api.model
    def create(self, vals_list):
        self.sale_create_seq_name(vals_list)
        res = super().create(vals_list)
        return res

    def get_year(self, rec=None):
        year = str(datetime.datetime.now().year)[2:4]
        if rec:
            year = str(parser.parse(rec.get('date_order')).year)[-2:] if rec.get('date_order') else str(year)
        return year

    def get_month(self, rec=None):
        month = datetime.datetime.now().month
        if rec:
            month = parser.parse(rec.get('date_order')).month if rec.get('date_order') else '0' + str(
                month) if month < 10 else str(month)
            if month in list(range(10)):
                return "0" + str(month)
            return month
        return None

    def sale_create_seq_name(self, vals_list=None):
        seq = self.env['ir.sequence'].next_by_code('sale.order.sequence').split("-")
        seqCO = self.env['ir.sequence'].next_by_code('sale.order.contract.sequence')

        next_num = 0
        short_name = str(self.env['res.partner'].browse(vals_list.get('partner_id')).short_name) if self.env[
            'res.partner'].browse(vals_list.get('partner_id')).short_name else ''
        if seq:
            partner = self.env['res.partner'].browse(vals_list.get('partner_id'))
            partner.so_partner_seq += 1
            next_num = partner.so_partner_seq
            name = self.get_new_name(seq, next_num, short_name, vals_list)
            is_exist = self.env['sale.order'].search([('name', '=', name)])
            if is_exist:
                self.sale_create_seq_name(vals_list)
            else:
                vals_list['name'] = name

        if seqCO:
            partner = self.env['res.partner'].browse(vals_list.get('partner_id'))
            partner.co_partner_seq += 1
            next_num = partner.co_partner_seq
            name = self.get_new_name(seqCO, next_num, short_name, vals_list)
            is_exist = self.env['sale.order'].search([('deal_ref', '=', name)])
            if is_exist:
                self.sale_create_seq_name(vals_list)
            else:
                vals_list['hidden_ref'] = name.split("-")[0] + "-" + name.split("-")[2]

    def get_new_name(self, seq=None, next_num=None, short_name=None, rec=None):
        month = self.get_month(rec)
        year = self.get_year(rec)
        if next_num in list(range(10)):
            name = short_name + "-" + seq[1] + "-" + year + "" + str(month)
            get_seq_name = self.check_in_partner_seq(name)
            return get_seq_name
        else:
            name = short_name + "-" + seq[1] + "-" + year + "" + str(month)
            get_seq_name = self.check_in_partner_seq(name)
            return get_seq_name

    def check_in_partner_seq(self, name=None):
        partner_seq_obj = self.env['partner.sequence']
        # is_exists = partner_seq_obj.search([('name', '=', name)])
        is_exists = partner_seq_obj.search([('name', '=', name), ('company_id', '=', self.env.company.id)])

        if is_exists:
            if "PFI" in name:
                new_name = is_exists.name + str(is_exists.next_number).zfill(3)
            else:
                new_name = is_exists.name + str(is_exists.next_number).zfill(2)

            is_exists.next_number += 1
            return new_name
        else:
            # if there is no company id in record and the current company id is kemexon id
            # then it means that we should get the is_kem_seq next number
            is_kem_seq = partner_seq_obj.search([('name', '=', name), ('company_id', '=', False)])
            if is_kem_seq and self.env.company.id == 1:
                is_kem_seq.next_number += 1
                if "PFI" in name:
                    new_name = is_kem_seq.name + str(is_kem_seq.next_number).zfill(3)
                else:
                    new_name = is_kem_seq.name + str(is_kem_seq.next_number).zfill(2)
                return new_name
            else:
                num = 1
                if "PFI" in name:
                    new_name = name + str(num).zfill(3)
                else:
                    new_name = name + str(num).zfill(2)
                num += 1
                partner_seq_obj.create({
                    'name': name,
                    'next_number': num,
                    'company_id': self.env.company.id
                })
                return new_name

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for rec in self:
            rec.deal_ref = rec.hidden_ref
            if rec.picking_ids:
                rec.picking_ids.write({'deal_ref': rec.deal_ref})
        return res


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    pv_count = fields.Float("Pv Count")
    rv_count = fields.Float("Pv Count")
    sequence_done = fields.Boolean("Sequence Done", copy=False)

    def action_post(self):
        for rec in self:
            if not rec.sequence_done:
                rec.generate_payment_sequence()
        return super().action_post()

    def generate_payment_sequence(self):
        if self.payment_type != 'outbound':
            seq = self.env['ir.sequence'].next_by_code('payment.receive.sequence')
            check_name = self.check_exist(seq)
            if check_name:
                self.generate_payment_sequence()
            else:
                self.name = None
                self.name = seq
                self.sequence_done = True
        else:
            seq = self.env['ir.sequence'].next_by_code('payment.voucher.sequence')
            check_name = self.check_exist(seq)
            if check_name:
                self.generate_payment_sequence()
            else:
                self.name = None
                self.name = seq
                self.sequence_done = True

    def check_exist(self, seq=None):
        return self.env['account.payment'].search([('name', '=', seq)])


class InheritResCustomer(models.Model):
    _inherit = 'res.partner'

    inv_partner_seq = fields.Integer("Invoice Sequence")
    inv_prov_partner_seq = fields.Integer("Provisional Invoice Sequence")
    bill_partner_seq = fields.Integer("Bill Sequence")
    bill_prov_partner_seq = fields.Integer("Provisional Bill Sequence")
    credit_partner_seq = fields.Integer("Credit Note Sequence")
    refund_partner_seq = fields.Integer("Refund Sequence")
    picking_partner_seq = fields.Integer("Picking Sequence")
    so_partner_seq = fields.Integer("SO Sequence")
    co_partner_seq = fields.Integer("Contract Sequence")


class PartnerSequence(models.Model):
    _name = 'partner.sequence'

    name = fields.Char("Name")
    next_number = fields.Integer("Next Number", default=1)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
