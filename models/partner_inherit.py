# en models/__init__.py importa este archivo
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = "res.partner"

    vape_loyalty_moves_ids = fields.One2many(
        "vape.loyalty.point.move", "partner_id", string="Movimientos de Puntos", copy=False
    )

    vape_available_points = fields.Integer(
        string="Puntos disponibles", compute="_compute_vape_available_points", store=False
    )

    def _compute_vape_available_points(self):
        Move = self.env["vape.loyalty.point.move"]
        for p in self:
            p.vape_available_points = Move.get_partner_available_points(p.commercial_partner_id, p.company_id or self.env.company)
