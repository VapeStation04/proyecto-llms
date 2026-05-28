{
    'name': 'Vape POS Order Fields',
    'version': '2.2',
    'category': 'Sales/Point of Sale',
    'summary': 'Agrega campos personalizados (Canales, Tipo de envío, etc.) al POS.',
    'description': """
        Este módulo extiende el Punto de Venta nativo para cumplir con los flujos B2C:
        - Selección de Canales (Rappi, Saga Falabella, Web, Wsp, etc.)
        - Selección de Tipo de Envío (Express, Regular, Shalom, Recojo en tienda)
        - Adaptación de Métodos de Pago
        - Persistencia del dato del canal en los reembolsos
    """,
    'author': 'Frank Condor',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order_views.xml',
        'views/vape_channel_views.xml',
        'views/vape_shipping_type_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [

            'vape_pos_order_fields/static/src/app/components/custom_grid_popup.js',
            'vape_pos_order_fields/static/src/app/store/pos_store.js',
            'vape_pos_order_fields/static/src/app/models/pos_order.js',
            'vape_pos_order_fields/static/src/app/screens/payment_screen.js',
            
            'vape_pos_order_fields/static/src/xml/custom_grid_popup.xml', 
            'vape_pos_order_fields/static/src/xml/custom_menu_button.xml',
            'vape_pos_order_fields/static/src/xml/summary_box.xml',
            'vape_pos_order_fields/static/src/xml/payment_screen.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}