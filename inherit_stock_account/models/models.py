# -*- coding: utf-8 -*-

from odoo import models


class InheritStockAccount(models.Model):
    _inherit = 'account.move.line'

    def _get_stock_valuation_layers_price_unit(self, layers):
        price_unit_by_layer = {}
        for layer in layers:
            price_unit_by_layer[layer] = layer.value / layer.quantity if layer.quantity else layer.value
        return price_unit_by_layer
