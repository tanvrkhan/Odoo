from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    analytic_distribution_formatted_sol = fields.Char(
        string='Analytic',
        compute='_compute_analytic_distribution_formatted_sol',
        store=True, default=''
    )

    def _compute_analytic_distribution_formatted_sol(self):
        for record in self:
            analytic_distribution = record.analytic_distribution
            if analytic_distribution:
                formatted = []
                for account_id, value in analytic_distribution.items():
                    accounts = self.env['account.analytic.account'].search([('id', '=', account_id)])
                    account_names = [account.name for account in accounts]
                    formatted.append(f"{', '.join(account_names)}")
                record.analytic_distribution_formatted_sol = ', '.join(formatted)
            else:
                record.analytic_distribution_formatted_sol = ''
