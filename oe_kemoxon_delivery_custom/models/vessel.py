from odoo import models, fields, api


class Vessel(models.Model):
    _name = "vessel"
    vessel_name = fields.Char()
    imo = fields.Char()
    owner = fields.Char()

    def name_get(self):
        return [(vessel.id, "{} ({})".format(vessel.vessel_name, vessel.imo)) for vessel in self]
