# Copyright 2023 Aures Tic - Jose Zambudio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
            WITH max_order AS (
                SELECT pos_order.session_id as session_id,
                    MAX(pos_order.sequence_number) as sequence_number
                FROM pos_order
                GROUP BY pos_order.session_id
            )
            UPDATE pos_session
            SET sequence_number = max_order.sequence_number
            FROM max_order
            WHERE pos_session.id = max_order.session_id
        """,
    )
