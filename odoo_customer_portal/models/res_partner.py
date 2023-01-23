# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'customer_rank desc, name'

    customer_reg = fields.Boolean(default=False, string="customer Registered", copy=False)

    def _increase_rank(self, field, n=1):
        res = super(ResPartner, self)._increase_rank(field, n=n)
        if self.ids and field in ['customer_rank']:
            for partner in self:
                if not partner.customer_reg:
                    user_obj = self.env["res.users"].search([('login', '=', partner.email)], limit=1)
                    if user_obj and user_obj.has_group('base.group_portal') and partner.customer_rank:
                        user_obj.partner_id.customer_reg = True
                    else:
                        user_obj.partner_id.customer_reg = False
        return res


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        if user.partner_id and user.partner_id.customer_rank:
            user.partner_id.sudo().customer_reg = True
        else:
            user.partner_id.sudo().customer_reg = False
        return user

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        for user in self:
            if user.active and user.has_group('base.group_portal') and user.partner_id.customer_rank:
                user.partner_id.sudo().customer_reg = True
            else:
                user.partner_id.sudo().customer_reg = False
        return res
