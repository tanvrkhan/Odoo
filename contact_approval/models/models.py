# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('reject', 'Reject')
        ],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )

    def approve(self):
        for rec in self:
            rec.status = 'approved'
            rec.active = True

    def reject(self):
        for rec in self:
            rec.status = 'reject'
            rec.active = False

    def draft(self):
        for rec in self:
            rec.status = 'draft'
            rec.active = False

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        res.active = False
        res.status = 'draft'
        return res
