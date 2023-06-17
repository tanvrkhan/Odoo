# -*- coding: utf-8 -*-
{
    'name': "Profit And Loss",
    'summary': """
        Profit And Loss View, sale, purchase and expense
    """,
    'description': """
        Profit And Loss View, sale, purchase and expense
    """,
    'author': "OdooERP.ae",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'purchase', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
