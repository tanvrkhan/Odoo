# -*- coding: utf-8 -*-
{
    'name': "Kemexon Financial Instruments",
    'author': 'Kemexon IT Dxb',

    'summary': 'Kemexon Financial Instruments',

    'description': """
        Kemexon Financial Instruments
    """,

    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Kemexon',
    'version': '0.1',
    'sequence': 10,
    # any module necessary for this one to work correctly
    'depends': ['product', 'sale', 'purchase', 'account', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bank_financing_limits_views.xml',
        'views/fi_lc_views.xml',
        'views/fi_lc_lines_views.xml',
        'views/purchase_order_inherited_view.xml',
        'views/res_bank_inherited_view.xml',
        'views/sale_order_inherited_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
