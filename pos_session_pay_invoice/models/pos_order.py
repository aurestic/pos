from odoo import api, models
from odoo.osv.expression import AND


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def search_paid_order_ids(self, config_id, domain, limit, offset):
        with_ref_domain = [
            ("pos_reference", "!=", False),
        ]
        new_domain = AND([domain, with_ref_domain])
        return super(PosOrder, self).search_paid_order_ids(
            config_id,
            new_domain,
            limit,
            offset,
        )
