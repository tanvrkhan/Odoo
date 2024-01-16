# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Restriction on Users',
    'version': '16.0.0.0',
    'category': 'Sales',
    'summary': 'This odoo app helps businesses to restrict access to specific products, or product categories for particular users by assigning products or product categories to specific users and limit access to sensitive products and prevent unauthorized sales.',
    'description': """
        Product Restriction on Users Odoo app is designed to help businesses to streamline their sales processes by providing greater control over product visibility by restricting access to specific products, or product categories for particular users. Businesses can control who has access to different products and product categories by assigning products or product categories to specific users. With this app, businesses can limit access to sensitive products and prevent unauthorized sales.
        
        Product Restriction on Users in odoo,
        Allow Products to Users in odoo,
        Allow Product Category to Users in odoo,
        Selected Products to Users in odoo,
        Selected Product Category to Users in odoo,

    """,
    "author": "BrowseInfo",
    "price": 20,
    "currency": 'EUR',
    "website" : "https://www.browseinfo.com",
    'depends': ['base','sale_management'],
    'data': [
            'security/base_groups.xml',
            'views/res_user_view.xml',
    ],
    'license': 'OPL-1',
    "auto_install": False,
    "installable": True,
    'live_test_url':'https://youtu.be/WjHueq7xtSs',
    "images":['static/description/Banner.gif'],
}
