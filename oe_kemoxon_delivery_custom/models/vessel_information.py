from odoo import models, fields, api


class VesselInformation(models.Model):
    _name="vessel.information"
    vessel_id = fields.Many2one("vessel","Vessel")
    bl_date=fields.Date("BL Date")
    cp_date= fields.Date("CP Date")
    confimation_date=fields.Date("Confirmation Date")
    loadport_agent= fields.Many2one("res.partner",string="Loadport agent")
    disport_agent=fields.Many2one("res.partner",string="Disport agent")
    loadport_inspectors=fields.Many2one("res.partner",string="Loadport Inspectors")
    disport_inspectors=fields.Many2one("res.partner",string="Disport Inspectors")
    demurrage_rate =fields.Float("Demurrage Rate")
    stock_pick_ids = fields.Many2one("stock.picking", string="Vessels Details", required=True)
    loadport = fields.Many2one("delivery.location","Load Port")
    disport = fields.Many2one("delivery.location","Disport")
    country_of_origin=fields.Many2one("res.country","Country of origin")


    def name_get(self):
        return [(vessel.id, "{} ({})".format(vessel.vessel_id.vessel_name, vessel.vessel_id.imo,vessel.bl_date)) for vessel in self]
