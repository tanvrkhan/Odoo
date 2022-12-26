# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import base64


class AccountMove(models.Model):
    _inherit = "account.move"

    deal_ref = fields.Char("Deal Ref")
    bill_date = fields.Date("B/L Date", related='picking_id.bill_date')
    vessel_name = fields.Char("Vessel Name", related='picking_id.vessel_name')
    delivery_location = fields.Many2one('delivery.location', "Delivery Location",
                                        related='picking_id.delivery_location')
    picking_id = fields.Many2one('stock.picking', "Delivery Order")

    journal_id = fields.Many2one('account.journal', string='Journal', domain=[], required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True)

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
                if 0 <= due_days >= 30:
                    zero_thirty = invoice.amount_residual
                elif 31 <= due_days >= 60:
                    thirtyone_sixty = invoice.amount_residual
                elif 61 <= due_days >= 90:
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

    def action_send_aged_balance_invoice_report(self, move_type):
        if move_type == 'out_invoice':
            sow_template_id = self.env.ref('oe_kemexon_custom.email_template_aged_balance_invoice_report')
            invoices = self.env['account.move'].search(
                [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
        else:
            sow_template_id = self.env.ref('oe_kemexon_custom.email_template_aged_balance_bill_report')
            invoices = self.env['account.move'].search(
                [('amount_residual', '>', 0), ('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
        # sow_report_id = self.env.ref('oe_kemexon_custom.action_report_aged_balance')
        # generated_report = \
        #     self.env['ir.actions.report']._render_qweb_pdf("oe_kemexon_custom.action_report_aged_balance", self.id)[0]
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
                                    <tr>
                                        <th>Customer</th>
                                        <th>Reference</th>
                                        <th>Currency</th>
                                        <th>Due Date</th>
                                        <th>Due Days</th>
                                        <th>Total Amount</th>
                                        <th>Balance</th>
                                        <th>0-30 Days</th>
                                        <th>31-60 Days</th>
                                        <th>61-90 Days</th>
                                        <th>Over 90 Days</th>
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
                if 0 <= due_days >= 30:
                    zero_thirty = invoice.amount_residual
                elif 31 <= due_days >= 60:
                    thirtyone_sixty = invoice.amount_residual
                elif 61 <= due_days >= 90:
                    sixteeone_nineteen = invoice.amount_residual
                else:
                    nineteen_above = invoice.amount_residual
                total_amount_total += invoice.amount_total
                total_amount_due += invoice.amount_residual
                total_zero_thirty += zero_thirty
                total_thirtyone_sixty += thirtyone_sixty
                total_sixteeone_nineteen += sixteeone_nineteen
                total_nineteen_above += nineteen_above

                body_html += '''<tr><td>''' + str(invoice.partner_id.short_name) + '''</td> <td>''' + str(
                    invoice.name) + '''</td><td>''' + str(
                    invoice.currency_id.name) + '''</td><td>''' + str(invoice.invoice_date_due) + '''</td><td>''' + str(
                    due_days) + '''</td><td>''' + str(invoice.amount_total) + '''</td><td>''' + str(
                    invoice.amount_residual) + '''</td><td>''' + str(
                    zero_thirty) + '''</td><td>''' + str(thirtyone_sixty) + '''</td><td>''' + str(
                    sixteeone_nineteen) + '''</td><td>''' + str(nineteen_above) + '''</td></tr>'''

        sow_template_id.body_html = body_html
        sow_template_id.send_mail(self.id, force_send=True)

    def action_send_customer_reminder(self):
        yesterday = fields.Date.today() - datetime.timedelta(days=1)
        invoices = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
             ('invoice_date_due', '=', yesterday)])
        over_due_template = self.env.ref('oe_kemexon_custom.email_template_customer_reminder')
        print(invoices,'invoicesinvoicesinvoicesinvoices')
        for invoice in invoices:
            email_values = {
                'email_to': invoice.partner_id.email or 'abcd@gmail.com'
            }
            over_due_template.send_mail(invoice.id, force_send=True, email_values=email_values)


class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")
