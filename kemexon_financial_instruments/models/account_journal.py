from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    tf_account = fields.Boolean(string='Trade Finance Account')
