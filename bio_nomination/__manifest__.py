# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Biofin Nomination',
    'version': '15.0.1.0.7',
    'author': 'Eezee-It',
    'category': 'Sale',
    # 'description': 'Biofin NOMINATION v15.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'uom',
        'sale_management',
        'purchase',
        'stock',
        'sales_team',
        'sale_stock',
    ],
    'data': [
        'report/bio_nomination_report_templates.xml',
        'data/bio_nomination_type_data.xml',
        'data/bio_nomination_mail_data.xml',
        'data/bio_nomination_cost_type_data.xml',
        'security/ir.model.access.csv',
        'views/bio_nomination_views.xml',
        'views/bio_vessel.xml',
        'views/bio_nomination_cost_type.xml',
        'wizard/bio_nomination_send_views.xml',
        'views/uom.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/product_template.xml',
        'views/product_product.xml',
        'views/bio_nomination_menuitem.xml',
    ],
}
