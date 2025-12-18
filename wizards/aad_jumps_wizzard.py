from odoo import models, fields
from odoo.exceptions import UserError


class RiggingAADJumpsWizard(models.TransientModel):
    _name = "rigging.aad.jumps.wizard"
    _description = "Component / AAD jumps wizard"

    # -------------------------
    # Campos del wizard
    # -------------------------
    component_id = fields.Many2one(
        "rigging.component",
        string="Component",
        required=True,
    )
    rig_id = fields.Many2one(
        "rigging.rig",
        string="Rig",
        required=True,
    )
    action_type = fields.Selection(
        [
            ("mount", "Mount"),
            ("unmount", "Unmount"),
        ],
        required=True,
        default="mount",
    )

    # Lectura actual del AAD que mete el usuario
    aad_jumps = fields.Char(
        string="AAD jumps",
        required=True,
    )

    # Opcional, por si quieres mostrar algo en el futuro
    current_jumps = fields.Integer(
        string="Current jumps",
        readonly=True,
        help="Current reference jumps (for information only).",
    )

    # -------------------------
    # Helpers internos
    # -------------------------

    def _get_rig_components(self, rig):
        """Devuelve TODOS los componentes montados en un rig como recordset."""
        comps = self.env["rigging.component"].browse()
        if rig.canopy_id:
            comps |= rig.canopy_id
        if rig.container_id:
            comps |= rig.container_id
        if rig.reserve_id:
            comps |= rig.reserve_id
        if rig.aad_id:
            comps |= rig.aad_id

        # solo los que realmente están montados en ese rig
        return comps.filtered(lambda c: c.rig_id.id == rig.id and c.is_mounted)

    def _set_component_on_rig(self, comp, rig, mount=True):
        """Sincroniza el componente con el slot correcto del rig."""
        if not rig:
            return

        if comp.component_type == "canopy":
            rig.canopy_id = comp if mount else False
        elif comp.component_type == "container":
            rig.container_id = comp if mount else False
        elif comp.component_type == "reserve":
            rig.reserve_id = comp if mount else False
        elif comp.component_type == "aad":
            rig.aad_id = comp if mount else False

    def _clear_component_from_all_rigs(self, comp):
        """Por seguridad: elimina el componente de cualquier rig donde esté en algún slot."""
        Rig = self.env["rigging.rig"]
        rigs = Rig.search([
            "|", "|", "|",
            ("canopy_id", "=", comp.id),
            ("container_id", "=", comp.id),
            ("reserve_id", "=", comp.id),
            ("aad_id", "=", comp.id),
        ])
        for rig in rigs:
            if rig.canopy_id.id == comp.id:
                rig.canopy_id = False
            if rig.container_id.id == comp.id:
                rig.container_id = False
            if rig.reserve_id.id == comp.id:
                rig.reserve_id = False
            if rig.aad_id.id == comp.id:
                rig.aad_id = False

    # -------------------------
    # Acción principal
    # -------------------------

    def action_confirm(self):
        self.ensure_one()
        comp = self.component_id
        rig = self.rig_id

        if not comp:
            raise UserError("No component selected.")
        if not rig:
            raise UserError("No rig selected.")

        # ▶ Validar que el usuario ha puesto saltos
        if not self.aad_jumps:
            raise UserError("Please enter the AAD jumps.")

        try:
            aad_jumps = int(self.aad_jumps)
        except ValueError:
            raise UserError("AAD jumps must be a number.")

        # ----------------- MOUNT -----------------
        if self.action_type == "mount":
            # 1) componentes actualmente montados en el rig (menos reserve)
            comps_to_touch = self._get_rig_components(rig).filtered(
                lambda c: c.component_type != "reserve"
            )

            # 2) añadimos también el componente que estamos montando,
            #    si no es reserve y aún no está en la lista
            if comp.component_type != "reserve" and comp not in comps_to_touch:
                comps_to_touch |= comp

            # 3) para todos esos componentes: reset + set de jumps_on_mount
            for c in comps_to_touch:
                c.jumps_on_mount = 0
                c.jumps_on_mount = aad_jumps

            # 4) si el componente es AAD -> total_jumps = aad_jumps SOLO para el AAD
            if comp.component_type == "aad":
                comp.total_jumps = aad_jumps

            # 5) AHORA sí: marcar montado y enlazar rig
            if comp.rig_id != rig or not comp.is_mounted:
                comp.write({
                    "rig_id": rig.id,
                    "is_mounted": True,
                })
                self._set_component_on_rig(comp, rig, mount=True)

        # ----------------- UNMOUNT -----------------
        else:
            # componentes canopy/container montados en este rig
            canopy_container = self._get_rig_components(rig).filtered(
                lambda c: c.component_type in ("canopy", "container")
            )

            if comp.component_type == "aad":
                # actualizar saltos de canopy y container
                for c in canopy_container:
                    delta = aad_jumps - (c.jumps_on_mount or 0)
                    c.total_jumps = (c.total_jumps or 0) + delta
                    c.jumps_on_mount = 0

                # actualizar el propio AAD
                comp.total_jumps = aad_jumps
                comp.jumps_on_mount = 0

            elif comp.component_type in ("canopy", "container"):
                delta = aad_jumps - (comp.jumps_on_mount or 0)
                comp.total_jumps = (comp.total_jumps or 0) + delta
                comp.jumps_on_mount = 0

            # recordar rig actual antes de limpiar
            old_rig = comp.rig_id

            # marcar desmontado en el componente
            comp.write({
                "rig_id": False,
                "is_mounted": False,
            })

            # limpiar slot del rig
            if old_rig:
                self._set_component_on_rig(comp, old_rig, mount=False)

        return {"type": "ir.actions.act_window_close"}
