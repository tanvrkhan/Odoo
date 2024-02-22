# Copyright 2022 Eezee-IT (<http://www.eezee-it.com> - info@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'BIO Profile',
    'version': '15.0.1.0.1',
    'license': 'LGPL-3',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Profile',
    # 'description': 'Install BIO modules',
    'depends': [
        'base',
        'bio_sale',
        'bio_purchase',
        'bio_nomination',
        'bio_account',
    ],

    'demo': [],
    'data': [
        'data/company_data.xml',
    ],
    'active': False,
    'installable': True,
    'auto_install': False,
    'application': True,
}
