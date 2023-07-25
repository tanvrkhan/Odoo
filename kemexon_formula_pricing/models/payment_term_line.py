from odoo import fields, models, api


class PaymentTermLine(models.Model):
    _inherit = 'account.payment.term.line'
    document_description= fields.Char()