# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

{
    'name': 'Account Cancel Invoice/Journal Entries',
    'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Accounting',
    'description':
        """
        odoo app allow to cancel account invoice and cancel journal entries for specific users.
        
        Account cancel invoice 
        Account vendro bills 
        Cancel Journal entries 
        Odoo Cancel customer invoice
        Odoo cancel vendor bill
        odoo cancel supplier invoice
        odoo journal entries 
        odoo cancel moves 
        odoo cancel right account
        odoo account cancel rights
        odoo accounting move cancel rights
        Account cancel rights
        Odoo account cancel rights
        For Helping allow user can cancel access right.
        Odoo For Helping allow user can cancel access right.
        this apps use to allow users are cancel invoice.
        Odoo this apps use to allow users are cancel invoice.
        Account cancel
        Odoo account cancel
        Cancel customer invoice
        Odoo cancel customer invoice
        Cancel vendor bill
        Odoo cancel vendor bill
        Cancel journal entry
        Odoo cancel journal entry
        Manage account cancel
        Odoo manage account sales
        Manage cancel customer invoice
        Odoo mange cancel customer invoice
        Manage cancel vendor bill
        Odoo manage cancel vendor bill
        Manage cancel journal entry
        Odoo manage cancel journal entry

Introducing the Odoo app that offers precise control over account invoice and journal entry cancellations, tailored for specific users' permissions. This app empowers you to restrict cancellation access with precision, ensuring that only authorized users can perform these critical actions. Maintain data integrity and financial accuracy effortlessly with our intuitive solution. Streamline your workflow and enhance security with the ultimate cancellation control app for Odoo.

Odoo account management, Invoice cancellation app, Journal entry management, Financial record control, Authorized user functionality, Cancel customer invoices, Void vendor bills, Revoke journal entries, Seamless accounting processes, Financial data accuracy, Odoo app for cancellations, Accounting flexibility, Accurate financial records, Streamlined invoice management, Efficient journal entry handling, Financial control software, Invoice voiding solution, Vendor bill management, User-friendly cancellation app, Enhanced accounting control

    """,
    'summary': 'odoo app allow to cancel account invoice and cancel journal entries for specific users | cancel invoice allows only access user | Cancel account invoice | cancel vendor bill | cancel journal entries | cancel customer invoice | cancel invoice | Odoo account management | Invoice cancellation app | Journal entry management | Financial record control | Authorized user functionality | Cancel customer invoices| Void vendor bills | Revoke journal entries| Seamless accounting processes | Financial data accuracy | Odoo app for cancellations | Accounting flexibility | Accurate financial records | Streamlined invoice management | Efficient journal entry handling | Financial control software | Invoice voiding solution | Vendor bill management| User-friendly cancellation app | Enhanced accounting control',
    'depends': ['account'],
    'data': [
        'security/security_file.xml',
        'views/account_views.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':20.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
