# -*- encoding: utf-8 -*-
# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class SaleCertficate(models.Model):
    _name = "sale.certificate"
    _description = "Certification"
    name = fields.Char()
