from odoo import fields, api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    fi_lc_ids = fields.Many2one('fi.lc', string='Financial Instruments')
