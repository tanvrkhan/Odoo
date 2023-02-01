from odoo import api, fields, models, _
import datetime
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'ir.attachment'

    expiry_date = fields.Date('Expiry Date')

    def action_send_customer_reminder(self):
        one_month_before = fields.Date.today() + relativedelta(months=1)
        attachments = self.search([('res_model', '=', 'res.partner'), ('expiry_date', '=', one_month_before)])
        email_template = self.env.ref('odoo_customer_portal.email_template_attachment_expiry')
        for attachment in attachments:
            if attachment.res_id:
                partner = self.env['res.partner'].browse(attachment.res_id)
                if partner:
                    email_values = {
                        'email_to': partner.email or 'abcd@gmail.com'
                    }
                    email_template.send_mail(attachment.id, force_send=True, email_values=email_values)

    def action_send_customer_remindesr(self):
        yesterday = fields.Date.today() - datetime.timedelta(days=1)
        after_three_day = fields.Date.today() + datetime.timedelta(days=3)
        invoices_1_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
             ('invoice_date_due', '=', yesterday)])
        over_due_template = self.env.ref('oe_kemoxon_delivery_custom.email_template_attachment_expiry')
        for invoice1 in invoices_1_day:
            email_values = {
                'email_to': invoice1.partner_id.email or 'abcd@gmail.com'
            }
            over_due_template.send_mail(invoice1.id, force_send=True, email_values=email_values)

        # friendly_reminder

        invoices_3_day = self.env['account.move'].search(
            [('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
             ('invoice_date_due', '=', after_three_day)])
        friendly_reminder_template = self.env.ref(
            'oe_kemoxon_delivery_custom.email_template_friendly_reminder_reminder')
        for invoice3 in invoices_3_day:
            email_values = {
                'email_to': invoice3.partner_id.email or 'abcd@gmail.com'
            }
            friendly_reminder_template.send_mail(invoice3.id, force_send=True, email_values=email_values)
