from odoo import models

class PosOrder(models.Model):
    _inherit = "pos.order"

    def action_pos_order_paid(self):
        """Al pagar el pedido POS, se generan puntos de fidelidad."""
        res = super().action_pos_order_paid()

        LoyaltyMove = self.env["vape.loyalty.point.move"]

        for order in self:
            partner = order.partner_id
            if not partner or order.amount_total <= 0:
                continue

            # Por ejemplo: 1 punto por cada 10 de moneda gastada
            points = int(order.amount_total / 10)

            if points > 0:
                LoyaltyMove.earn_points(
                    partner=partner,
                    points=points,
                    origin_model="pos.order",
                    origin_ref=f"POS-{order.name}",
                    days_valid=90,  # expiran en 90 días
                    company=order.company_id,
                )

        return res
