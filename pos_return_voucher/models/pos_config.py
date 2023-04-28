from odoo import _, api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    return_voucher_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Return voucher IDs Sequence",
        readonly=True,
        help="This sequence is automatically created by Odoo but you can "
        "change it to customize the reference numbers of your return vouchers.",
        copy=False,
        ondelete="restrict",
    )
    return_voucher_validity = fields.Integer(
        default=30,
    )

    @api.model
    def _get_return_voucher_sequence_vals(self, name, company_id=False):
        return {
            "name": _("POS Return Voucher %s", name),
            "padding": 4,
            "prefix": "%s/" % name,
            "code": "pos.return.voucher",
            "company_id": company_id,
        }

    @api.model
    def create(self, values):
        IrSequence = self.env["ir.sequence"].sudo()
        val = self._get_return_voucher_sequence_vals(
            values["name"], company_id=values.get("company_id", False)
        )
        values["return_voucher_sequence_id"] = IrSequence.create(val).id
        return super(PosConfig, self).create(values)
