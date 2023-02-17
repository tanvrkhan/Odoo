# -*- coding: utf-8 -*-
{
    'name': "contacts_import_fields",

    'summary': """
        All the custom fields added to contacts for initial import.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kemexon",
    'website': "https://www.kemexon.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Kemexon',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
