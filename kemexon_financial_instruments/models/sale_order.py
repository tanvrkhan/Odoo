from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fi_lc_ids = fields.Many2one('fi.lc', string='FI LC')
