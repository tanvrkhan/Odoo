# -*- coding: utf-8 -*-
{
    'name': "Sequence Modification",
    'summary': """This module is all about sequence modification""",
    'description': """In this module we modify the sequence invoice, bill and 
    delivery
    """,
    'author': "OKLAND",
    'website': "http://www.yourcompany.com",
    'category': 'Kemexon',
    'version': '0.1',
    'depends': ['base', 'account', 'sale', 'stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/invoice_seq.xml',
        'data/bill_seq.xml',
        'data/delivery_seq.xml',
        'data/credit_note.xml',
        'data/payment_receive.xml',
        'data/receitp_se.xml',
        'data/sale_order_seq.xml',
        'data/debit_seq.xml',
        'data/payment_voucher_seq.xml',
        'data/journel_entry_seq.xml',
        'views/partner_seq.xml',
    ],

}
