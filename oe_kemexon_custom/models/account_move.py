# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
        invoices = self.env['account.move'].search([('amount_residual', '>', 0)])
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
                    'nineteen_above': nineteen_above
                }
                result.append(data_dict)
        data = {
            'result': result,
            'total_amount_total': total_amount_total,
            'total_amount_due': total_amount_due,
            'total_zero_thirty': total_zero_thirty,
            'total_thirtyone_sixty': total_thirtyone_sixty,
            'total_sixteeone_nineteen': total_sixteeone_nineteen,
            'total_nineteen_above': total_nineteen_above
        }
        return data

    def action_send_aged_balance_report(self):
        sow_template_id = self.env.ref('oe_kemexon_custom.email_template_aged_balance_report')
        sow_report_id = self.env.ref('oe_kemexon_custom.action_report_aged_balance')
        generated_report = \
            self.env['ir.actions.report']._render_qweb_pdf("oe_kemexon_custom.action_report_aged_balance", self.id)[0]
        data_record = base64.b64encode(generated_report)
        ir_values = {
            'name': 'Aged Balance',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'account.move',
        }
        report_attachment = self.env['ir.attachment'].sudo().create(ir_values)
        sow_template_id.attachment_ids = [(6, 0, [report_attachment.id])]
        sow_template_id.send_mail(self.id, force_send=True)


class DeliveryLocation(models.Model):
    _name = "delivery.location"

    name = fields.Char("Name")
