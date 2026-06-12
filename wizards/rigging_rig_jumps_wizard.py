from odoo import models, fields
from odoo.exceptions import UserError


class RigJumpsWizard(models.TransientModel):
    _name = "rigging.rig.jumps.wizard"
    _description = "Rig - Update All Jumps wizard"

    rig_id = fields.Many2one(
        "rigging.rig",
        string="Rig",
        required=True,
        readonly=True,
    )

    # Lo que el usuario introduce (no queremos default 0)
    aad_jumps = fields.Char(
        string="AAD jumps",
        required=True,
        help="Enter the current AAD jumps (number).",
    )

    def action_confirm(self):
        """Actualiza saltos en TODOS los componentes del rig (excepto reserve)."""
        self.ensure_one()

        if not self.rig_id:
            raise UserError("No rig selected.")

        self.rig_id.action_update_all_jumps(self.aad_jumps)

        # Cerrar el wizard
        return {"type": "ir.actions.act_window_close"}