from odoo import api, fields, models
from bs4 import BeautifulSoup


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    @staticmethod
    def get_text_from_html_field(doc):
        if doc.invoice_payment_term_id.note:
            text = ' '.join(BeautifulSoup(doc.invoice_payment_term_id.note, "html.parser").findAll(text=True))
            return text
        else:
            return None


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    @staticmethod
    def get_text_from_html_field(doc):
        if doc.payment_term_id.note:
            text = ' '.join(BeautifulSoup(doc.payment_term_id.note, "html.parser").findAll(text=True))
            return text
        else:
            return None
