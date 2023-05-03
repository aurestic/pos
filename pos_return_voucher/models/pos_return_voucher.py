from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


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
    reamining_amount = fields.Float(
        compute="_compute_reamining_amount",
        store=True,
        readonly=True,
    )
    redeemed_order_ids = fields.Many2many(
        comodel_name="pos.order",
        relation="pos_order_return_voucher_rel",
        column1="return_voucher_id",
        column2="order_id",
        string="Redeemed on order",
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
            order = rec.order_id
            state = "active"
            if float_is_zero(
                rec.reamining_amount, precision_rounding=order.currency_id.rounding
            ):
                state = "done"
            elif now > rec.max_validity_date:
                state = "expired"
            rec.state = state

    @api.depends("amount", "redeemed_order_ids", "redeemed_order_ids.payment_ids")
    def _compute_reamining_amount(self):
        for rec in self:
            return_voucher = rec.redeemed_order_ids.payment_ids.filtered(
                lambda payment: (
                    payment.payment_method_id.return_voucher and payment.amount > 0
                )
            )
            rec.reamining_amount = rec.amount - sum(return_voucher.mapped("amount"))
