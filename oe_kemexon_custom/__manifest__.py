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
    'depends': ['account', 'base','sale','sale_stock','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'report/aged_balance_report.xml',
        'report/delivery_sale_invoice_template.xml',
        'report/report.xml',
        'data/mail_template_data.xml',
        'data/crone.xml',
        'report/invoice_report_template.xml',
        'report/pro-forma_invoice_template.xml',
        'views/account_move_views.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/trucktransportdetails.xml',
        'wizard/kemexon_aging_balance_report_view.xml',
        'views/res_partner_bank_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
