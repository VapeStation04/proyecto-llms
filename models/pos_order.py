from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    vs_channel_id = fields.Many2one(
        comodel_name='vape.channel',
        string='Canal de Venta'
    )
    
    vs_shipping_type_id = fields.Many2one(
        comodel_name='vape.shipping.type',
        string='Tipo de Envío'
    )

    vape_payment_methods = fields.Char(
        string='Métodos de Pago', 
        compute='_compute_vape_payment_methods'
    )

    @api.depends('payment_ids', 'payment_ids.payment_method_id')
    def _compute_vape_payment_methods(self):
        for order in self:
            methods = order.payment_ids.mapped('payment_method_id.name')
            order.vape_payment_methods = ', '.join(methods) if methods else 'Sin pago'

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super()._order_fields(ui_order)
        
        if ui_order.get('vs_channel_id'):
            order_fields['vs_channel_id'] = ui_order.get('vs_channel_id')
            
        if ui_order.get('vs_shipping_type_id'):
            order_fields['vs_shipping_type_id'] = ui_order.get('vs_shipping_type_id')
            
        return order_fields