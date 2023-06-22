# -*- coding: utf-8 -*-
{
    'name': 'Estimate Module',
    'version': '16.0.0.1',
    'summary': 'Estimate Module',
    'description': """
        Estimate Module
        """,
    'category': 'Accounting',
    'website': 'https://www.yourcompany.com',
    'depends' : ['base', 'mail', 'oe_kemoxon_delivery_custom'],
    'data': [
        'security/ir.model.access.csv',
        'views/estimate_module_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'reports/reports.xml',
        'data/data.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'estimate_module/static/src/css/purchase_form_width.css',
            'estimate_module/static/src/css/sales_form_width.css',
            'estimate_module/static/src/css/costs_form_width.css',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
