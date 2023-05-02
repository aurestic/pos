from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    emitted_return_voucher_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="order_id",
        string="Emitted return voucher",
    )
    redeemed_return_voucher_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="redeemed_order_id",
        string="Redeemed return vouchers",
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
            self.emitted_return_voucher_ids |= PosReturnVoucher.browse(
                data.get("redeemed_return_voucher_id", False)
            ).exists()
        elif payment_method.return_voucher and data.get("redeemed_return_voucher_id"):
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
