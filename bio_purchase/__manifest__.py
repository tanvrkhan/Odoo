# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Biofin Purchase',
    'version': '15.0.1.0.1',
    'author': 'Eezee-It',
    'category': 'Purchase',
    # 'description': 'Biofin Purchase v15.0',
    'license': 'LGPL-3',
    'depends': [
        'bio_sale',
        'purchase',
        'stock',
        'purchase_stock'
    ],
    'data': [
        'views/purchase_order_views.xml',
    ],
}
