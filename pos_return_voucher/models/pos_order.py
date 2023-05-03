from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    emitted_return_voucher_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="order_id",
        string="Emitted return voucher",
        readonly=True,
    )
    redeemed_return_voucher_ids = fields.Many2many(
        comodel_name="pos.return.voucher",
        relation="pos_order_return_voucher_rel",
        column1="order_id",
        column2="return_voucher_id",
        string="Redeemed return vouchers",
        readonly=True,
    )

    def add_payment(self, data):
        PosReturnVoucher = self.env["pos.return.voucher"]
        payment_method = self.env["pos.payment.method"].browse(
            data.get("payment_method_id", False)
        )
        if payment_method.return_voucher and not data.get("redeemed_return_voucher_id"):
            # emitted
            return_voucher = PosReturnVoucher.create(
                {
                    "order_id": data.get("pos_order_id"),
                    "amount": abs(data.get("amount")),
                }
            )
            data["emitted_return_voucher_id"] = return_voucher.id
            self.emitted_return_voucher_ids |= return_voucher
        elif payment_method.return_voucher:
            # redeemed
            self.redeemed_return_voucher_ids |= PosReturnVoucher.browse(
                data.get("redeemed_return_voucher_id", False)
            ).exists()
        return super(PosOrder, self).add_payment(data)

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        fields = super(PosOrder, self)._payment_fields(order, ui_paymentline)
        fields.update(
            {
                "emitted_return_voucher_id": ui_paymentline.get(
                    "emitted_return_voucher_id", False
                ),
                "redeemed_return_voucher_id": ui_paymentline.get(
                    "redeemed_return_voucher_id", False
                ),
            }
        )
        return fields
