from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fi_lc_id = fields.Many2one('fi.lc', string='Financial Instruments')
