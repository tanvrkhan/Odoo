from odoo import models


class KemexonAgingBalanceReport(models.TransientModel):
    _name = 'kemexon.aging.balance.report'

    def action_print_invoice_report(self):
        invoice = self.env['account.move'].search([('amount_residual', '>', 0), ('move_type', '=', 'out_invoice')],
                                                  limit=1)
        return self.env.ref('oe_kemoxon_delivery_custom.action_report_aged_balance').report_action(invoice)

    def action_print_bill_report(self):
        invoice = self.env['account.move'].search([('amount_residual', '>', 0), ('move_type', '=', 'in_invoice')],
                                                  limit=1)
        return self.env.ref('oe_kemoxon_delivery_custom.action_report_aged_balance').report_action(invoice)
