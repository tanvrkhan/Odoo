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


