from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    analytic_distribution_formatted = fields.Char(
        string='Analytic',
        compute='_compute_analytic_distribution_formatted',
        store=True,
        readonly=True
    )

    @api.depends('analytic_distribution')
    def _compute_analytic_distribution_formatted(self):
        for record in self:
            analytic_distribution = record.analytic_distribution
            if analytic_distribution:
                formatted = []
                for account_id, value in analytic_distribution.items():
                    accounts = self.env['account.analytic.account'].search([('id', '=', account_id)])
                    account_names = [account.name for account in accounts]
                    formatted.append(f"{', '.join(account_names)}")
                record.analytic_distribution_formatted = ', '.join(formatted)
            else:
                record.analytic_distribution_formatted = ''

