# -*- coding: utf-8 -*-
{
    'name': "Analytic Summary Accounts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kemexon",
    'website': "https://www.kemexon.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Kemexon',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','purchase','oe_kemoxon_delivery_custom'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
