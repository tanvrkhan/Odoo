# -*- coding: utf-8 -*-
{
    'name': "Contacts Approval",
    'summary': """Contacts Approval""",
    'description': """
        Contacts Approval
    """,
    'author': "odooerp.ae",
    'website': "",
    'category': 'Uncategorized',
    'version': '16.0.0.1',
    'depends': ['base', 'contacts'],
    'data': [
        'security/contact_approval.xml',
        'views/views.xml',
    ]
}
