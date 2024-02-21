# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BioNomination(models.Model):
    _name = "bio.nomination.line"
    _description = "bio_nomination_line"

    product_id = fields.Many2one('product.product')
    qty = fields.Float(digits=(16, 3))
    qty_done = fields.Float(digits=(16, 3))
    nomination_id = fields.Many2one('bio.nomination')
    product_packaging_qty = fields.Float('Packaging Quantity')
    product_packaging_id = fields.Many2one('product.packaging', string='Packaging',
                                           domain="[ ('product_id','=',product_id)]")
