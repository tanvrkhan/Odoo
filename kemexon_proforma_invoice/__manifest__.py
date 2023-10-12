# -*- coding: utf-8 -*-
{
    'name': "kemexon_proforma_invoice",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'sale', 'sale_management', 'stock', 'sale_stock', 'purchase','hr', 'oe_kemoxon_delivery_custom', 'kemexon_formula_pricing'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/proforma_invoice_view.xml',
        'views/proforma_invoice_line_view.xml',
        'views/sale_order_inherit_view.xml',
        'report/proforma_invoice_screen_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
