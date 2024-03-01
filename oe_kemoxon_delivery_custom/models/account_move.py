# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import base64
from operator import itemgetter


class AccountMove(models.Model):
    _inherit = "account.move"

    fusion_reference = fields.Char("Fusion Ref")
    fusion_invoice_ref = fields.Char("Fusion Invoice Ref")
    fusion_location = fields.Char('Fusion Location')
    fusion_trader = fields.Char('Fusion Trader')
    fusion_bl_date = fields.Date('Fusion BL Date')
    fusion_delivery_from = fields.Date('Fusion Delivery From')
    fusion_delivery_to = fields.Date('Fusion Delivery To')
    fusion_ncv = fields.Char('Fusion NCV')
    fusion_loadport = fields.Char('Fusion Load Port')
    fusion_disport = fields.Char('Fusion Discharge Port')
    fusion_country_of_origin = fields.Char('Fusion COO')
    fusion_contract_ref = fields.Char('Fusion Contract Ref')
    fusion_imo = fields.Char('Fusion IMO')
    fusion_vessel_name = fields.Char('Fusion Vessel Name')
    fusion_deal_ref = fields.Char('Fusion Deal Ref')
    fusion_payment_term = fields.Char('Fusion Payment Term')
    fusion_representing_entity = fields.Char('Fusion Representing Entity')
    fusion_retermsandconditions = fields.Char('Fusion RE Terms and Conditions')
    fusion_retaxid = fields.Char('Fusion RE Tax ID')
    contract_ref = fields.Char('Contract Reference')
    deal_ref = fields.Char("Deal Ref")
    bill_date = fields.Date("B/L Date", related='picking_id.bill_date')
    tt_date = fields.Date("TT Date", related='picking_id.tt_date')
    vessel_name = fields.Char("Vessel Name", related='picking_id.vessel_name')
    delivery_location = fields.Many2one('delivery.location', "Delivery Location",
                                        related='picking_id.delivery_location')
    picking_id = fields.Many2one('stock.picking', string='Delivery Order', domain="[('id', 'in', picking_domain_ids)]",
                                 readonly=False, store=True)
    picking_domain_ids = fields.Many2many('stock.picking', compute='_compute_picking_id2', invisible=True)

    vessel_information_id = fields.Many2one('vessel.information', "Vessel Details")
    vessel_name = fields.Char("Vessel Name", related='vessel_information_id.vessel_id.vessel_name', store=True, readonly=False)
    imo = fields.Char("IMO", related='vessel_information_id.vessel_id.imo', store=True, readonly=False)
    ncv = fields.Char("NCV")
    loadport = fields.Many2one("delivery.location", "Load port", related='vessel_information_id.loadport', store=True, readonly=False)
    disport = fields.Many2one("delivery.location", "Discharge port", related='vessel_information_id.disport', store=True, readonly=False)
    country_of_origin = fields.Many2one("res.country", "COO", related='vessel_information_id.country_of_origin', store=True, readonly=False)
    payment_notes = fields.Char("Payment Notes")
    bl_date = fields.Date("BL Date", related='vessel_information_id.bl_date', store=True, readonly=False)
    cod_date = fields.Date("COD Date", related='vessel_information_id.cod_date')
    nor_date = fields.Date("NOR Date", related='vessel_information_id.nor_date')
    # bill_date = fields.Date("B/L Date", related='picking_id.bill_date')
    # vessel_name = fields.Char("Vessel Name", related='picking_id.vessel_name')
    payment_notes = fields.Text()
    delivery_notes = fields.Text()
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[], required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True)
    show_delivery_to = fields.Boolean(string="Show Delivery To", default=False)
    delivery_to = fields.Date(string="Delivery Till", default=False)
    delivery_from = fields.Date(string="Delivery From", default=False)
    show_delivery_to = fields.Boolean(string="Show Delivery To", default=False)
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    transporter_details_id = fields.Many2one('stock.picking', 'Transporter Delivery')

    payment_terms_id2 = fields.Many2one('account.payment.term', 'Payment terms')
    incoterm_location_custom = fields.Many2one('incoterm.location', string='Incoterm Location',
                                               readonly=False,
                                               stored=True)
    trader = fields.Many2one('hr.employee', string='Trader', related='picking_id.trader', store=True, readonly=False)
    legal_entity = fields.Many2one('legal.entity', string='Representing Entity')
    en_plus = fields.Boolean('EN Plus')
    show_hs_code = fields.Boolean('Show HS Code')
    updatestatus=fields.Char()
    
    
    
    company_bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Company Bank Account',
        readonly=False,
        stored=True
    )
    
    @api.onchange('picking_id')
    def on_change_picking_id(self):
        for record in self:
            record.incoterm_location_custom = record.picking_id.incoterm_location_custom
    @api.onchange('partner_id')
    def on_change_partner_id(self):
        for record in self:
            record.company_bank_account_id= record.partner_id.company_bank_account_id
    
    def action_post(self):
        for rec in self:
            if rec.move_type == 'out_invoice':
                if not rec.partner_id.company_bank_account_id:
                    raise UserError(
                        _("Bank is not selected for this customer. Please select a bank for the customer before posting the invoice."))
            return super(AccountMove, rec).action_post()

    @api.depends('invoice_line_ids.sale_line_ids.move_ids.picking_id')
    def _compute_picking_id2(self):
        for invoice in self:
            pickings = invoice.invoice_line_ids.sale_line_ids.move_ids.mapped('picking_id')
            invoice.picking_domain_ids = pickings
    def reset_to_draft(self):
        self.updatestatus='waspostedbefore'
        res = super().button_draft()
        
        return res
    
    def update_costing_from_svl_to_bill(self):
        for record in self:
            if record.move_type == 'in_invoice':
                total_quantity = 0
                total_amount = 0
                for al in record.line_ids:
                    if al.purchase_line_id:
                        if al.purchase_line_id.move_ids:
                            for sm in al.purchase_line_id.move_ids:
                                if sm.stock_valuation_layer_ids:
                                    if sm.state == 'done':
                                        for vl in sm.stock_valuation_layer_ids:
                                            if vl.quantity > 0:
                                                total_quantity += vl.quantity
                                                total_amount += vl.value
                base_currency = record.company_id.currency_id
                if total_quantity!=0:
                    cost_currency= total_amount/total_quantity
                    cost_usd = record.currency_id._convert(
                        cost_currency,
                        base_currency, record.company_id, record.date, True)
                    record.state = 'draft'
                    self.env['account.move.line'].search([('move_id', '=', record.id),('display_type','=','cogs')]).unlink()
                    storedquantityrecord= self.env['account.move.line'].search([('move_id', '=', record.id),('quantity','!=','0')])
                    storedquantity=storedquantityrecord.quantity
                    for ae in record.line_ids:
                        ae.remove_move_reconcile()

                        if ae.amount_currency != 0:
                            newquantity=0
                            if ae.amount_currency > 0:
                                if ae.quantity == 0:
                                    newquantity = storedquantity
                                if newquantity < 0:
                                    newquantity = newquantity * -1
                                else:
                                    newquantity = ae.quantity
                                storedquantity=newquantity
                                ae.with_context(
                                    check_move_validity=False).amount_currency = cost_currency * newquantity
                                ae.with_context(
                                    check_move_validity=False).debit = cost_usd * newquantity
                            elif ae.amount_currency < 0:
                                newquantity=0
                                if ae.quantity == 0:
                                    newquantity = storedquantity
                                if newquantity > 0:
                                    newquantity = newquantity * -1
                                else:
                                    newquantity = newquantity
                               
                                ae.with_context(
                                    check_move_validity=False).amount_currency = cost_currency * newquantity
                                ae.with_context(
                                    check_move_validity=False).credit = cost_usd * newquantity * -1
                    record.state = 'posted'
            
    def get_invoice_details(self):
        invoices = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', self.move_type), ('state', '=', 'posted')])
        today_date = fields.Date.today()
        'short_name'
        result = []
        total_amount_total = 0
        total_amount_due = 0
        total_zero_thirty = 0
        total_thirtyone_sixty = 0
        total_sixteeone_nineteen = 0
        total_nineteen_above = 0
        for invoice in invoices:
            if invoice.invoice_date_due and invoice.invoice_date_due < today_date:
                due_days = (today_date - invoice.invoice_date_due).days
                zero_thirty = 0
                thirtyone_sixty = 0
                sixteeone_nineteen = 0
                nineteen_above = 0
                if 0 <= due_days <= 30:
                    zero_thirty = invoice.amount_residual
                elif 31 <= due_days <= 60:
                    thirtyone_sixty = invoice.amount_residual
                elif 61 <= due_days <= 90:
                    sixteeone_nineteen = invoice.amount_residual
                else:
                    nineteen_above = invoice.amount_residual
                total_amount_total += invoice.amount_total
                total_amount_due += invoice.amount_residual
                total_zero_thirty += zero_thirty
                total_thirtyone_sixty += thirtyone_sixty
                total_sixteeone_nineteen += sixteeone_nineteen
                total_nineteen_above += nineteen_above

                data_dict = {
                    'short_name': invoice.partner_id.short_name,
                    'reference': invoice.name,
                    'currency': invoice.currency_id.name,
                    'due_date': invoice.invoice_date_due,
                    'due_days': due_days,
                    'amount_total': invoice.amount_total,
                    'amount_due': invoice.amount_residual,
                    'zero_thirty': zero_thirty,
                    'thirtyone_sixty': thirtyone_sixty,
                    'sixteeone_nineteen': sixteeone_nineteen,
                    'nineteen_above': nineteen_above,
                    'currency_id': invoice.currency_id
                }
                result.append(data_dict)
        USD = self.env['res.currency'].search([('name', '=', 'USD')])
        base_currency = self.env.company.currency_id
        result = sorted(result, key=itemgetter('due_days'), reverse=True)
        data = {
            'result': result,
            'total_amount_total': round(base_currency.compute(total_amount_total, USD), 2),
            'total_amount_due': round(base_currency.compute(total_amount_due, USD), 2),
            'total_zero_thirty': round(base_currency.compute(total_zero_thirty, USD), 2),
            'total_thirtyone_sixty': round(base_currency.compute(total_thirtyone_sixty, USD), 2),
            'total_sixteeone_nineteen': round(base_currency.compute(total_sixteeone_nineteen, USD), 2),
            'total_nineteen_above': round(base_currency.compute(total_nineteen_above, USD), 2),
            'usd_currency': USD,
            'partner': 'Customer' if self.move_type == 'out_invoice' else "Vendor"
        }
        return data
    
    def update_transit_account_from_product_categories(self):
        for rec in self:
            for line in rec.line_ids:
                if line.account_id.id == 2248:
                    if rec.move_type == 'out_invoice':
                        if line.product_id.type == 'product':
                            updated_account = line.product_id.categ_id.property_stock_account_output_categ_id
                            line.account_id = updated_account.id
                    if rec.move_type == 'in_invoice':
                        if line.product_id.type == 'product':
                            updated_account = line.product_id.categ_id.property_stock_account_input_categ_id
                            line.account_id = updated_account.id
    def action_send_aged_balance_invoice_report(self, move_type):
        if move_type == 'out_invoice':
            sow_template_id = self.env.ref('oe_kemoxon_delivery_custom.email_template_aged_balance_invoice_report')
            invoices = self.env['account.move'].search(
                [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
        else:
            sow_template_id = self.env.ref('oe_kemoxon_delivery_custom.email_template_aged_balance_bill_report')
            invoices = self.env['account.move'].search(
                [('amount_residual', '>', 0), ('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
        # sow_report_id = self.env.ref('oe_kemoxon_delivery_custom.action_report_aged_balance')
        # generated_report = \
        #     self.env['ir.actions.report']._render_qweb_pdf("oe_kemoxon_delivery_custom.action_report_aged_balance", self.id)[0]
        # data_record = base64.b64encode(generated_report)
        # ir_values = {
        #     'name': 'Aged Balance',
        #     'type': 'binary',
        #     'datas': data_record,
        #     'store_fname': data_record,
        #     'mimetype': 'application/pdf',
        #     'res_model': 'account.move',
        # }
        # report_attachment = self.env['ir.attachment'].sudo().create(ir_values)
        # sow_template_id.attachment_ids = [(6, 0, [report_attachment.id])]

        body_html = '''<h6>Customer Aging Balance Report</h6>
         As at &#160; %s
                            <br/>
                                                                                   <table class="table table-sm o_main_table" name="invoice_line_table">
                                                                               <thead>
                                    <tr style="border-bottom:2px solid #d4d6d9;border-top:2px solid #d4d6d9; border-top:2px solid #d4d6d9">
                                        <th>Customer</th>
                                        <th>Reference</th>
                                        <th>Currency</th>
                                        <th>Due Date</th>
                                        <th>Due Days</th>
                                        <th style="text-align:right;">Total Amount</th>
                                        <th style="text-align:right;">Balance</th>
                                        <th style="text-align:right;">0-30 Days</th>
                                        <th style="text-align:right;">31-60 Days</th>
                                        <th style="text-align:right;">61-90 Days</th>
                                        <th style="text-align:right;">Over 90 Days</th>
                                    </tr>
                                </thead>
                                                                              <tbody>
                                                                               ''' % (datetime.date.today(),)

        today_date = fields.Date.today()
        'short_name'
        result = []
        total_amount_total = 0
        total_amount_due = 0
        total_zero_thirty = 0
        total_thirtyone_sixty = 0
        total_sixteeone_nineteen = 0
        total_nineteen_above = 0
        for invoice in invoices:
            if invoice.invoice_date_due and invoice.invoice_date_due < today_date:
                due_days = (today_date - invoice.invoice_date_due).days
                zero_thirty = 0
                thirtyone_sixty = 0
                sixteeone_nineteen = 0
                nineteen_above = 0
                if 0 <= due_days <= 30:
                    zero_thirty = invoice.amount_residual
                elif 31 <= due_days <= 60:
                    thirtyone_sixty = invoice.amount_residual
                elif 61 <= due_days <= 90:
                    sixteeone_nineteen = invoice.amount_residual
                else:
                    nineteen_above = invoice.amount_residual
                total_amount_total += invoice.amount_total
                total_amount_due += invoice.amount_residual
                total_zero_thirty += zero_thirty
                total_thirtyone_sixty += thirtyone_sixty
                total_sixteeone_nineteen += sixteeone_nineteen
                total_nineteen_above += nineteen_above

                body_html += '''<tr style="border-bottom:2px solid #d4d6d9;border-top:2px solid #d4d6d9; border-top:2px solid #d4d6d9"><td>''' + str(
                    invoice.partner_id.short_name) + '''</td> <td>''' + str(
                    invoice.name) + '''</td><td>''' + str(
                    invoice.currency_id.name) + '''</td><td>''' + str(invoice.invoice_date_due) + '''</td><td>''' + str(
                    due_days) + '''</td><td style="text-align:right;">''' + str('{:0,.2f}'.format(
                    invoice.amount_total)) + '''</td><td  style='color:red;text-align:right;'>''' + str(
                    '{:0,.2f}'.format(invoice.amount_residual)) + '''</td><td style="text-align:right;">''' + str(
                    '{:0,.2f}'.format(zero_thirty)) + '''</td><td style="text-align:right;">''' + str(
                    '{:0,.2f}'.format(thirtyone_sixty)) + '''</td><td style="text-align:right;">''' + str(
                    '{:0,.2f}'.format(sixteeone_nineteen)) + '''</td><td style="text-align:right;">''' + str(
                    '{:0,.2f}'.format(nineteen_above)) + '''</td></tr>'''

        sow_template_id.body_html = body_html
        sow_template_id.send_mail(self.id, force_send=True)

    def get_total(self, total=None):
        number = "{:.2f}".format(total)
        return "{:,.2f}".format(float(number))

    def action_send_customer_reminder(self):
        yesterday = fields.Date.today() - datetime.timedelta(days=1)
        after_three_day = fields.Date.today() + datetime.timedelta(days=3)
        over_due_template = self.env.ref('oe_kemoxon_delivery_custom.email_template_customer_reminder')

        invoices_1_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'),
             ('state', '=', 'posted'),
             ('invoice_date_due', '=', yesterday), ('company_id', '=', 1)])
        for invoice1 in invoices_1_day:
            if invoice1.partner_id.id not in over_due_template.not_send_ids.ids:
                # email_values = {
                #     'email_to': invoice1.partner_id.email or 'abcd@gmail.com'
                # }
                over_due_template.send_mail(invoice1.id, force_send=True)
            else:
                continue

        # # friendly_reminder
        friendly_reminder_template = self.env.ref(
            'oe_kemoxon_delivery_custom.email_template_friendly_reminder_reminder')

        invoices_3_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'),
             ('state', '=', 'posted'),
             ('invoice_date_due', '=', after_three_day), ('company_id', '=', 1)])
        for invoice3 in invoices_3_day:
            if invoice3.partner_id.id not in friendly_reminder_template.not_send_ids.ids:
                # email_values = {
                #     'email_to': invoice1.partner_id.email or 'abcd@gmail.com'
                # }
                friendly_reminder_template.send_mail(invoice3.id, force_send=True)
            else:
                continue

    def action_send_customer_reminder_sa(self):
        yesterday = fields.Date.today() - datetime.timedelta(days=1)
        after_three_day = fields.Date.today() + datetime.timedelta(days=3)
        over_due_template = self.env.ref('oe_kemoxon_delivery_custom.email_template_customer_reminder_sa')

        invoices_1_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'),
             ('state', '=', 'posted'),
             ('invoice_date_due', '=', yesterday), ('company_id', '=', 2)])
        for invoice1 in invoices_1_day:
            if invoice1.partner_id.id not in over_due_template.not_send_ids.ids:
                # email_values = {
                #     'email_to': invoice1.partner_id.email or 'abcd@gmail.com'
                # }
                over_due_template.send_mail(invoice1.id, force_send=True)
            else:
                continue

        # # friendly_reminder
        friendly_reminder_template = self.env.ref(
            'oe_kemoxon_delivery_custom.email_template_friendly_reminder_reminder_sa')

        invoices_3_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'),
             ('state', '=', 'posted'),
             ('invoice_date_due', '=', after_three_day), ('company_id', '=', 2)])
        for invoice3 in invoices_3_day:
            if invoice3.partner_id.id not in friendly_reminder_template.not_send_ids.ids:
                # email_values = {
                #     'email_to': invoice1.partner_id.email or 'abcd@gmail.com'
                # }
                friendly_reminder_template.send_mail(invoice3.id, force_send=True)
            else:
                continue


    @api.depends('needed_terms', 'invoice_date_due')
    def _compute_invoice_date_due(self):
        today = fields.Date.context_today(self)
        for move in self:
            if not move.invoice_date_due:
                move.invoice_date_due = move.needed_terms and max(
                    (k['date_maturity'] for k in move.needed_terms.keys() if k),
                    default=False,
                ) or today
    
    def update_costing(self):
        for record in self:
            avg_price = 0
            sale_line_ids=[]
            for line in record.line_ids:
                if line.sale_line_ids:
                    sale_line_ids += line.sale_line_ids
            for line in record.line_ids:
                if line.display_type =='cogs' and line.price_unit>0:
                    if sale_line_ids:
                        total_quantity = 0
                        total_amount = 0
                        for soline in sale_line_ids:
                            if line.product_id == soline.product_id:
                                if soline.move_ids:
                                    for sm in soline.move_ids:
                                        if sm.stock_valuation_layer_ids:
                                            if sm.state == 'done':
                                                for vl in sm.stock_valuation_layer_ids:
                                                    if vl.quantity < 0:
                                                        total_quantity += vl.quantity
                                                        total_amount += vl.value
                        if total_quantity != 0:
                            avg_price = round(total_amount / total_quantity, 2)
                        if record.reversed_entry_id:
                            original_line = record.move_id.reversed_entry_id.line_ids.filtered(
                            lambda l: l.display_type == 'cogs' and l.product_id == self.product_id and
                                      l.product_uom_id == self.product_uom_id and l.price_unit >= 0)
                            original_line = original_line and original_line[0]
                            avg_price = original_line.price_unit if original_line \
                                else avg_price
                if avg_price:
                    to_change_lines = self.env['account.move.line'].search([('product_id','=',line.product_id.id),('move_id','=',line.move_id.id),('display_type','=','cogs')])
                    for cline in to_change_lines:
                        cline.remove_move_reconcile()
                        if cline.amount_currency > 0:
                            cline.with_context(
                                check_move_validity=False).amount_currency = avg_price * cline.quantity
                            cline.with_context(
                                check_move_validity=False).price_unit = avg_price
                        elif cline.amount_currency < 0:
                            cline.with_context(
                                check_move_validity=False).amount_currency = avg_price * cline.quantity * -1
                            cline.with_context(
                                check_move_validity=False).price_unit = avg_price * -1
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    deduction = fields.Float('Deduction')

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id', 'deduction')
    def _compute_totals(self):
        for line in self:
            if line.display_type != 'product':
                line.price_total = line.price_subtotal = False
            # Compute 'price_subtotal'.
            line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
            subtotal = line.quantity * line_discount_price_unit

            # Compute 'price_total'.
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line_discount_price_unit,
                    quantity=line.quantity,
                    currency=line.currency_id,
                    product=line.product_id,
                    partner=line.partner_id,
                    is_refund=line.is_refund,
                )
                line.price_subtotal = taxes_res['total_excluded'] - line.deduction
                line.price_total = taxes_res['total_included'] - line.deduction
            else:
                line.price_total = line.price_subtotal = subtotal - line.deduction
    

class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")
