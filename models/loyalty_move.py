from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta

class LoyaltyPointMove(models.Model):
    _name = "vape.loyalty.point.move"
    _description = "Loyalty Point Move (Ledger)"
    _order = "expiry_date asc, id asc"

    state = fields.Selection([
        ("open", "Open"),
        ("consumed", "Consumed"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ], default="open", required=True)

    partner_id = fields.Many2one("res.partner", required=True, index=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    points = fields.Integer(required=True, help="Positive = earned, Negative = spent/adjust")
    expiry_date = fields.Date(help="Only meaningful for positive moves")
    origin_model = fields.Char()
    origin_ref = fields.Char(help="e.g., SO/INV/POS ref")

    # saldo disponible de este movimiento positivo
    remaining = fields.Integer(compute="_compute_remaining", store=True)
    is_positive = fields.Boolean(compute="_compute_is_positive", store=True)

    @api.depends("points")
    def _compute_is_positive(self):
        for rec in self:
            rec.is_positive = rec.points > 0

    @api.depends("points", "state")
    def _compute_remaining(self):
        for rec in self:
            # remaining solo aplica a positivos abiertos y no expirados/cancelados
            if rec.points > 0 and rec.state == "open":
                # calculamos consumo vinculado vía move lines (simple: calculado por negativos con origin_ref)
                consumed = sum(self.search([
                    ("partner_id","=",rec.partner_id.id),
                    ("company_id","=",rec.company_id.id),
                    ("points","<",0),
                    ("origin_ref","=",f"CONS_{rec.id}")
                ]).mapped(lambda m: -m.points))
                rec.remaining = max(0, rec.points - consumed)
            else:
                rec.remaining = 0

    # Util: total puntos disponibles del partner
    @api.model
    def get_partner_available_points(self, partner, company=None):
        company = company or self.env.company
        today = fields.Date.context_today(self)
        positives = self.search([
            ("partner_id","=",partner.id),
            ("company_id","=",company.id),
            ("points",">",0),
            ("state","=","open"),
            "|", ("expiry_date","=",False), ("expiry_date",">=",today),
        ])
        total = sum(p.remaining for p in positives)
        return int(total)

    # Cron: expirar
    @api.model
    def cron_expire_points(self):
        today = fields.Date.context_today(self)
        to_expire = self.search([
            ("points",">",0),
            ("state","=","open"),
            ("expiry_date","!=",False),
            ("expiry_date","<", today),
        ])
        to_expire.write({"state": "expired"})
        return True

    # Consumo FIFO
    @api.model
    def consume_points(self, partner, amount_points, company=None):
        company = company or self.env.company
        if amount_points <= 0:
            return 0
        available = self.get_partner_available_points(partner, company)
        if amount_points > available:
            raise UserError(_("No hay suficientes puntos disponibles (solicitados %d, disponibles %d).") % (amount_points, available))

        today = fields.Date.context_today(self)
        buckets = self.search([
            ("partner_id","=",partner.id),
            ("company_id","=",company.id),
            ("points",">",0),
            ("state","=","open"),
            "|", ("expiry_date","=",False), ("expiry_date",">=",today),
        ], order="expiry_date asc, id asc")

        to_consume = amount_points
        for b in buckets:
            if to_consume <= 0:
                break
            take = min(b.remaining, to_consume)
            if take > 0:
                # crear movimiento negativo apuntando al bucket
                self.create({
                    "partner_id": partner.id,
                    "company_id": company.id,
                    "points": -take,
                    "origin_model": "loyalty.consume",
                    "origin_ref": f"CONS_{b.id}",
                })
                # recomputará remaining; si quedó en 0 no marcamos consumed para permitir trazabilidad por si hay reversos
                to_consume -= take
        return amount_points - to_consume

    # Ganar puntos helper
    @api.model
    def earn_points(self, partner, points, origin_model, origin_ref, days_valid=30, company=None):
        company = company or self.env.company
        if points <= 0:
            return False
        exp = fields.Date.context_today(self) + timedelta(days=days_valid)
        return self.create({
            "partner_id": partner.id,
            "company_id": company.id,
            "points": int(points),
            "expiry_date": exp,
            "origin_model": origin_model,
            "origin_ref": origin_ref,
        })
