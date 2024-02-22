# Copyright 2023
# Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Biofin Account',
    'version': '15.0.1.0.1',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Accounting/Accounting',
    # 'description': 'Biofin Account v15.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'sale_stock'
    ],
    'data': [
        'views/account_move.xml',
        'views/report_invoice.xml',
    ]
}
