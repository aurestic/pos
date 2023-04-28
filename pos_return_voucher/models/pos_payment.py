from odoo import fields, models


class PosPayment(models.Model):
    _inherit = "pos.payment"

    pos_return_voucher_id = fields.Many2one(
        comodel_name="pos.return.voucher",
        readonly=True,
    )

    def _export_for_ui(self, payment):
        data = super(PosPayment, self)._export_for_ui(payment)
        data.update(
            {
                "return_voucher": payment.payment_method_id.return_voucher,
                "pos_return_voucher_id": payment.pos_return_voucher_id.id,
            }
        )
        return data
