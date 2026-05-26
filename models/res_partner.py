from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Float(
        string='Puntos de Fidelidad',
        compute='_compute_loyalty_points',
        store=False
    )

    @api.depends('vape_loyalty_point_move_ids.remaining')
    def _compute_loyalty_points(self):
        for partner in self:
            total = sum(partner.vape_loyalty_point_move_ids.filtered(lambda m: m.state == 'active').mapped('remaining'))
            partner.loyalty_points = total

    vape_loyalty_point_move_ids = fields.One2many(
        'vape.loyalty.point.move',
        'partner_id',
        string='Movimientos de Puntos'
    )
