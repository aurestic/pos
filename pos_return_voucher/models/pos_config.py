from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    return_voucher_validity = fields.Integer(
        default=30,
    )
