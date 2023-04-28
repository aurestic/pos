from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    return_voucher_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="order_id",
        string="Crated return voucher",
    )
    redeemed_return_voucher_ids = fields.One2many(
        comodel_name="pos.return.voucher",
        inverse_name="redeemed_order_id",
        string="Redeemed return vouchers",
    )

    def add_payment(self, data):
        PosReturnVoucher = self.env["pos.return.voucher"]
        super(PosOrder, self).add_payment(data)
        payment_method = self.env["pos.payment.method"].browse(
            data.get("payment_method_id", False)
        )
        if payment_method.return_voucher:
            if not data.get("pos_return_voucher_id"):
                # emitted
                self.return_voucher_ids |= PosReturnVoucher.create(
                    {
                        "order_id": data.get("pos_order_id"),
                        "amount": abs(data.get("amount")),
                    }
                )
            else:
                # redeemed
                self.redeemed_return_voucher_ids |= PosReturnVoucher.browse(
                    data.get("pos_return_voucher_id", False)
                ).exists()

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        fields = super(PosOrder, self)._payment_fields(order, ui_paymentline)
        fields.update(
            {
                "pos_return_voucher_id": ui_paymentline.get(
                    "pos_return_voucher_id", False
                ),
            }
        )
        return fields
