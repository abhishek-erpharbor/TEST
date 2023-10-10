# -*- coding: utf-8 -*-
{
    'name': 'EHCS Sale VIP Discount',
    'version' : '16.0.1.0.0',
    'summary': 'Sales',
    'category': 'Website Sales',
    'description': """
        Create VIP discount promo code and apply for actual customer
     """,
    'author': 'ERP Harbor Consulting Services',
    'website': 'https://www.erpharbor.com',
    'depends': ['website_sale', 'sale_management'],
    'data': [
        # security 
        'security/ir.model.access.csv',
        # Data
        'data/ir_cron_data.xml',
        # views
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/vip_discount_view.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
