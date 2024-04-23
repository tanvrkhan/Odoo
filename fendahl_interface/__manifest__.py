# -*- coding: utf-8 -*-
{
    'name': "Fendahl Interface",
    'summary': """""",
    'description': "Fendahl Interface",
    'author': "Kemexon",
    'website': "http://www.kemexon.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'account', 'sale', 'stock', 'purchase', 'oe_kemoxon_delivery_custom'],
    'data': [
        'data/data.xml',
        'views/partial_reconcile.xml',
        'views/trade_controller.xml',
        'views/cashflow_controller.xml',
        'views/transfer_controller.xml',
        'views/invoice_controller.xml',
        'views/nomination_controller.xml',
    ],

}
