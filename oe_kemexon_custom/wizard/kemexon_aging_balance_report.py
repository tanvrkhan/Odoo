from odoo import models


class KemexonAgingBalanceReport(models.TransientModel):
    _name = 'kemexon.aging.balance.report'

    def action_print_report(self):
        invoice = self.env['account.move'].search([],limit=1)
        return self.env.ref('oe_kemexon_custom.action_report_aged_balance').report_action(invoice)
