# -*- coding: utf-8 -*-
{
    "name": "Vape Loyalty Expiration",
    "version": "18.0.1.0.0",
    "author": "Sistemas Vape Station",
    "summary": "Puntos con vencimiento a 30 días, consumo FIFO(pila?)",
    "depends": ["base", "sale_management", "account", "point_of_sale"],  
    'data': [
        'security/ir.model.access.csv',
        'views/loyalty_move_view.xml',
        'views/res_partner_view.xml',
    ],
    "license": "OEEL-1",
    "installable": True,
    "application": True,
}
