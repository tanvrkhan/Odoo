from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_distribution_formatted_aml = fields.Char(
        string='Analytic',
        compute='_compute_analytic_distribution_formatted_aml',
        store=True, default=''
    )

    def _compute_analytic_distribution_formatted_aml(self):
        for record in self:
            analytic_distribution = record.analytic_distribution
            if analytic_distribution:
                formatted = []
                for account_id, value in analytic_distribution.items():
                    accounts = self.env['account.analytic.account'].search([('id', '=', account_id)])
                    account_names = [account.name for account in accounts]
                    formatted.append(f"{', '.join(account_names)}")
                record.analytic_distribution_formatted_aml = ', '.join(formatted)
            else:
                record.analytic_distribution_formatted_aml = ''
