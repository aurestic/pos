# Copyright 2023 Jose Zambudio - Aures Tic
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    IrSequence = env["ir.sequence"].sudo()

    for config in env["pos.config"].search([]):
        val = config._get_return_voucher_sequence_vals(
            config.name, company_id=config.company_id.id
        )
        config.return_voucher_sequence_id = IrSequence.create(val)
