from odoo import models, fields

class VapeChannel(models.Model):
    _name = 'vape.channel'
    _description = 'Canales de Venta Vape Station'

    active = fields.Boolean(string='Activo', default=True)

    name = fields.Char(string='Nombre del Canal', required=True)
    color = fields.Char(string='Color', default='#FF5733')
    icon = fields.Char(string='Ícono (FontAwesome)', default='fa-globe')
    
    custom_icon = fields.Image(
        string='Ícono Personalizado',
        max_width=256,
        max_height=256,
        help='Sube un SVG o PNG transparente en color blanco.'
    )
    
    pos_config_ids = fields.Many2many('pos.config', string='Puntos de venta')