from odoo import models, fields

class VapeShippingType(models.Model):
    _name = 'vape.shipping.type'
    _description = 'Tipos de Envío Vape Station'

    name = fields.Char(string='Tipo de Envío', required=True)

    active = fields.Boolean(string='Activo', default=True)
    
    pos_config_ids = fields.Many2many(
        comodel_name='pos.config',
        string='Puntos de venta'
    )