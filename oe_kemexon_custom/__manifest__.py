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
    'depends': ['account', 'base'],
    'data': [
        'report/invoice_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
