from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.name
            res.append((analytic.id, name))
        return res
