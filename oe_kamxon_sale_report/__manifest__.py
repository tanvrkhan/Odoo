# -*- coding: utf-8 -*-
{
    'name': "oe Kamxon Sale_report",

    'summary': """This module is all about""",

    'description': """
        Long description of module's purpose
    """,

    'author': "OKLAND",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/oe_invoice_report_temp.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
