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
        """Actualiza saltos en TODOS los componentes del rig (excepto reserve):

           total_jumps += aad_jumps - jumps_on_mount
           jumps_on_mount = aad_jumps
        """
        self.ensure_one()

        # --- Validación de la entrada ---
        if not self.aad_jumps:
            raise UserError("Please enter the AAD jumps.")

        try:
            aad_jumps = int(self.aad_jumps)
        except ValueError:
            raise UserError("AAD jumps must be a number.")

        if aad_jumps < 0:
            raise UserError("AAD jumps cannot be negative.")

        rig = self.rig_id
        if not rig:
            raise UserError("No rig selected.")

        Component = self.env["rigging.component"]

        # Todos los componentes montados en este rig menos la reserve
        comps = Component.search([
            ("rig_id", "=", rig.id),
            ("component_type", "!=", "reserve"),
        ])

        for comp in comps:
            if comp.component_type != "aad":
                #old_jom = comp.jumps_on_mount or 0
                if comp.last_jumps_update == 0:
                    delta = aad_jumps - (comp.jumps_on_mount or 0)
                else:
                    delta = aad_jumps - (comp.last_jumps_update or 0)
                    comp.last_jumps_update = aad_jumps

                comp.total_jumps = (comp.total_jumps or 0) + delta
                #comp.jumps_on_mount = aad_jumps
            else:
                comp.total_jumps = aad_jumps

        # Cerrar el wizard
        return {"type": "ir.actions.act_window_close"}