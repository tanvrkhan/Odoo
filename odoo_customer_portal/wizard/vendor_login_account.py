# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class VendorLoginAccount(models.TransientModel):
    _name = 'vendor.login.account'
    _description = "Vendor Login Account"

    def create_vendor_acocunt(self):
        self.ensure_one()
        ctx = dict(self.env.context or {})
        activeModel = ctx.get('active_model')
        activeId = ctx.get('active_id')
        if activeModel == 'res.partner':
            parnterObj = self.env['res.partner'].browse(activeId)
            if parnterObj.vendor_reg:
                self.env['res.users'].reset_password(parnterObj.email)
            else:
                userObj = self.env['res.users'].with_context(active_test=False).search([('login', '=', parnterObj.email)])
                if userObj:
                    if userObj.partner_id == parnterObj:
                        irModelData = self.env['ir.model.data']
                        templXmlId = irModelData._xmlid_to_res_id('base.group_portal')
                        userObj.write({
                            'groups_id': [(6, 0, [templXmlId])],
                            'active': True,
                        })
                        parnterObj.vendor_reg = True
                        userObj.reset_password(parnterObj.email)
                    else:
                        raise UserError(_("An user is already exist for the another partner with the same credentials i.e email."))
                else:
                    vals = {
                        'partner_id' : ctx.get('active_id'),
                        'login' : parnterObj.email,
                        'email' : parnterObj.email,
                        'password' : parnterObj.email,
                        'groups_id' : [(5,)]
                        }
                    userObj = self.env['res.users'].create(vals)
                    if userObj:
                        irModelData = self.env['ir.model.data']
                        templXmlId = irModelData._xmlid_to_res_id('base.group_portal')
                        res = userObj.write({'groups_id': [(6, 0, [templXmlId])]})
                        parnterObj.vendor_reg = True
        return True
