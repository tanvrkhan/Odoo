# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name": "Odoo Customer Portal",
    "summary": """The module allows you to provide a website portal to the customers so they can track and manage purchase orders directly from their account.""",
    "category": "Website",
    "version": "1.0.5",
    "sequence": 1,
    "author": "Webkul Software Pvt. Ltd.",
    "license": "Other proprietary",
    "website": "https://store.webkul.com/Odoo-customer-Portal.html",
    "description": """Odoo Customer Portal
Odoo Customer account on website
Odoo Customer website account
Manage purchase order from Customer account""",
    "live_test_url": "http://odoodemo.webkul.com/?module=odoo_customer_portal&lout=1&custom_url=/",
    "depends": [
        'sale',
        'website',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/crone.xml',
        'data/email_template.xml',
        'wizard/customer_login_account_view.xml',
        'views/ir_attchment_view.xml',
        'views/res_partner_view.xml',
        'views/portal_template.xml'
    ],
    "images": ['static/description/Banner.png'],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 99,
    "currency": "USD",
    # "assets"               :  {
    # 'web.assets_frontend':  [
    #                          'odoo_customer_portal/static/src/js/customer_portal.js',
    #                         ],
    #                         },
}
