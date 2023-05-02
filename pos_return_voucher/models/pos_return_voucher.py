from odoo import api, fields, models


class PosReturnVoucher(models.Model):
    _name = "pos.return.voucher"
    _description = "POS return voucher"
    _rec_name = "pos_reference"

    order_id = fields.Many2one(
        comodel_name="pos.order",
        string="Created from order",
        index=True,
        readonly=True,
    )
    date_order = fields.Datetime(
        related="order_id.date_order",
        readonly=True,
    )
    pos_reference = fields.Char(
        related="order_id.pos_reference",
        readonly=True,
    )
    max_validity_date = fields.Datetime(
        compute="_compute_max_validity_date",
        store=True,
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        default=lambda s: s.env.user,
    )
    amount = fields.Float(required=True, copy=False)
    redeemed_order_id = fields.Many2one(
        comodel_name="pos.order",
        string="Redeemed on order",
        index=True,
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ("active", "Active"),
            ("expired", "Expired"),
            ("done", "Done"),
        ],
        compute="_compute_state",
    )
    backorder_id = fields.Many2one(
        comodel_name="pos.return.voucher",
        string="Back Order of",
        copy=False,
        index=True,
        readonly=True,
        help="If this return voucher was split, then this field links to the "
        "return voucher which contains the already processed part.",
    )
    backorder_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="backorder_id",
        string="Back Orders",
    )

    @api.depends("order_id.date_order")
    def _compute_max_validity_date(self):
        for rec in self:
            if not rec.date_order:
                continue
            config = rec.order_id.session_id.config_id
            rec.max_validity_date = fields.Date.add(
                rec.date_order, days=config.return_voucher_validity
            )

    def _compute_state(self):
        now = fields.Datetime.now()
        for rec in self:
            state = "active"
            if rec.redeemed_order_id:
                state = "done"
            elif now > rec.max_validity_date:
                state = "expired"
            rec.state = state
