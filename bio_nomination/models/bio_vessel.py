# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BioVessel(models.Model):
    _name = "bio.vessel"
    _description = "Bio Vessel"

    name = fields.Char(string="Vessel Name", required="1")
    description = fields.Char(string="N°reg", required="1")
    partner_id = fields.Many2one('res.partner', 'Owner', required="1", domain="[('vessel_owner','=',True)]",
                                 context="{'default_vessel_owner':True}")
