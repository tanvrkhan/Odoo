# -*- coding: utf-8 -*-
{
    'name': "Line Items Tree Views",
    'author': 'Kemexon IT Dxb',

    'summary': 'Hospital Management System',

    'description': """
        Line Items Tree Views
    """,

    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Kemexon',
    'version': '0.1',
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['product', 'sale', 'purchase','oe_kemoxon_delivery_custom','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/line_items_tree_views.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
