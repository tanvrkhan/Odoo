# -*- coding: utf-8 -*-
{
    'name': 'OdooERP Delivery Custom',
    'version': '15.0.1.0.0',
    'sequence': 1,
    'description': """
OdooERP Sales
====================
""",
    'category': 'Kemexon',
    'author': 'OdooERP.ae, tou-odoo, Kemexon',
    'website': 'https://odooerp.ae/',
    'depends': ['account', 'base', 'sale', 'sale_management', 'sale_stock', 'purchase','hr','sh_warehouse_avg_costing'],
    'data': [
        'security/ir.model.access.csv',
        'report/aged_balance_report.xml',
        'report/delivery_sale_invoice_template.xml',
        'report/report.xml',
        'data/mail_template_data.xml',
        'data/data.xml',
        'data/crone.xml',
        'report/invoice_report_template.xml',
        'report/pro-forma_invoice_template.xml',
        'views/account_move_views.xml',
        'views/incoterm_location_view.xml',
        'views/region_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/trucktransportdetails.xml',
        'wizard/kemexon_aging_balance_report_view.xml',
        'views/res_partner_bank_view.xml',
        'views/vessel_views.xml',
        'views/vessel_information_views.xml',
        'views/product_template_view_inherit.xml',
        'views/legal_entity_views.xml',
        'wizard/message.xml',
        'views/stock_move_line.xml'
        # 'report/invoice_report_template_dry.xml',
        # menu_items
        # 'views/menu_items.xml',
        # actions
        # 'data/actions.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
