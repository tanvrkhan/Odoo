# -*- coding: utf-8 -*-
{
    'name': "Formula Pricing",
    'author': 'Kemexon IT Dxb',

    'summary': 'Formula Pricing',

    'description': """
        Formula Pricing
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
        'reports/pro-forma_invoice_template_inherited.xml',
        'reports/invoice_report_template_inherited.xml',
        'reports/fusion_invoice_report_template.xml',
        'views/product_template_field_view.xml',
        'views/account_move_view.xml',
        'views/sale_order_view.xml',
        'views/payment_terms.xml',
        'views/purchase_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
