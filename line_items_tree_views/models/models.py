# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class TruckTransportDetails(models.Model):
    _name = "truck.transport.details.view"
    _auto = False
    _rec_name = 'truck'

    transporter = fields.Many2one("res.partner", "Transporter")
    truck = fields.Char("Truck")
    trailer = fields.Char("Trailer")
    driver = fields.Char("Driver")
    passport = fields.Char("Passport")
    nominated = fields.Float(digits=(3, 3))
    loaded = fields.Float(digits=(3, 3))
    offloaded = fields.Float(digits=(3, 3))
    date = fields.Date('Date')
    status = fields.Selection(
        [("Nominated", "Nominated"), ("Waiting to load", "Waiting to load"), ("In transit", "In transit"),
         ("Waiting to offload", "Waiting to offload"), ("Completed", "Completed")], string="Status")
    statusdate = fields.Date("Status Date")
    picking_id = fields.Many2one('stock.picking', 'Delivery')
    stock_pick_ids = fields.Many2one("stock.picking", string="Truck Details", required=True)
    show_vat_ids = fields.Boolean(string="Show VAT Ids")
    seq = fields.Char("Sequence")

    def init(self):
        tools.drop_view_if_exists(self._cr, 'truck_transport_details_view')
        self._cr.execute(""" 
               CREATE OR REPLACE VIEW truck_transport_details_view AS ( 
                    SELECT row_number() OVER () as id,
                    tt.transporter as transporter,
                    tt.truck as truck,
                    tt.trailer as trailer,
                    tt.passport as passport,
                    tt.driver as driver,
                    tt.nominated as nominated,
                    tt.loaded as loaded,
                    tt.offloaded as offloaded,
                    tt.date as date,
                    tt.status as status,
                    tt.picking_id as picking_id,
                    tt.stock_pick_ids as stock_pick_ids,
                    tt.show_vat_ids as show_vat_ids,
                    tt.seq as seq,
                    tt.statusdate as statusdate
                    FROM truck_transport_details tt
                    LEFT JOIN  res_partner p ON tt.transporter = p.id
                    LEFT JOIN stock_picking sp on tt.stock_pick_ids = sp.id
                    LEFT JOIN stock_picking spd on tt.picking_id = spd.id
                    );
               """)
