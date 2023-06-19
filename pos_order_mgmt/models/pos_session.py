from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    sequence_number = fields.Integer(
        compute="_compute_sequence_number",
        store=True,
    )

    @api.depends("order_ids.sequence_number")
    def _compute_sequence_number(self):
        for session in self:
            if not session.order_ids:
                session.sequence_number = 1
                continue
            session.sequence_number = max(session.order_ids.mapped("sequence_number"))
