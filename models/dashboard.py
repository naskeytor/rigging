from odoo import models, fields

class RiggingDashboard(models.Model):
    _name = "rigging.dashboard"
    _description = "Rigging Dashboard"
    _auto = False  # <- no crea tabla, usaremos una VIEW

    name = fields.Char(readonly=True)

    def init(self):
        # Una VIEW con 1 registro (id=1) para que el kanban tenga “algo” que renderizar
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW rigging_dashboard AS (
                SELECT 1 AS id,
                       'Dashboard'::varchar AS name
            )
        """)