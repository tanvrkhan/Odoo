from odoo import fields, api, models


class BlanketOrder(models.Model):
    _inherit = 'purchase.requisition'

    vendor_ref = fields.Char('Vendor Reference')
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms',
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm', states={'done': [('readonly', True)]},
                                  help="International Commercial Terms are a series of predefined commercial terms "
                                       "used in international transactions.")

    analytic_accounts_summary = fields.Char(string='Analytic Accounts', compute='_summarize_analytics')

    def _summarize_analytics(self):
        for requisition in self:
            analytic_account_names = ''
            if requisition.line_ids:
                for line in requisition.line_ids:
                    if line.analytic_distribution:
                        analytic_account_keys = line.analytic_distribution.keys()
                        if analytic_account_keys:
                            analytic_value=''
                            for key in analytic_account_keys:
                                analytic_name = self.env['account.analytic.account'].search([('id', '=', key),])
                                for entry in analytic_name:
                                    if analytic_name:
                                        analytic_account_names=entry.name+', '+analytic_account_names
                    else:
                        requisition.analytic_accounts_summary=''
                requisition.analytic_accounts_summary = analytic_account_names
            else:
                requisition.analytic_accounts_summary = ''


class BlanketOrderLines(models.Model):
    _inherit = 'purchase.requisition.line'

    tolerance_type = fields.Selection([('min_max', 'Min/Max'), ('max', 'Max'), ('min', 'Min')],
                                      string="Tolerance Type")
    tolerance_percentage = fields.Float(string="Tolerance Percentage")


class BlanketSaleOrderLines(models.Model):
    _inherit = 'orderline.orderline'

