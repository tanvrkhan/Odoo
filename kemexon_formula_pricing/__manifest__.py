# -*- coding: utf-8 -*-
{
    'name': "Line Items Tree Views",
    'author': 'Kemexon IT Dxb',

    'summary': 'Line Items Tree Views',

    'description': """
        Line Items Tree Views
    """,

    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Kemexon',
    'version': '0.1',
    'sequence': 10,
    # any module necessary for this one to work correctly
    'depends': ['product', 'sale', 'purchase', 'oe_kemoxon_delivery_custom', 'account', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/invoice_report_template_inherited.xml',
        'views/product_template_field_view.xml',
        'views/account_move_view.xml',
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
