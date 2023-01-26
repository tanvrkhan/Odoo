# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def _eligible_for_qr_code(self, qr_method, debtor_partner, currency, raises_error=True):
        pass
