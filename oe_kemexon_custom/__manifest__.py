# -*- coding: utf-8 -*-
{
    'name': 'OdooERP Custom',
    'version': '15.0.1.0.0',
    'sequence': 1,
    'description': """
OdooERP Sales
====================
""",
    'category': 'Sales/Sales',
    'author': 'OdooERP.ae, tou-odoo',
    'website': 'https://odooerp.ae/',
    'depends': ['account', 'base','sale','sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report_template.xml',
        'report/pro-forma_invoice_template.xml',
        'views/account_move_views.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
