from odoo import models, fields, api
from odoo.exceptions import UserError


class Rig(models.Model):
    _name = "rigging.rig"
    _description = "Rig"
    _order = "number"

    # ------------------------------------------
    # CAMPOS PRINCIPALES
    # ------------------------------------------
    number = fields.Integer(string="Rig Number", required=True)

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        help="Owner of this rig and its mounted components.",
    )

    canopy_id = fields.Many2one(
        "rigging.component",
        string="Canopy",
        domain=[("component_type", "=", "canopy")],
    )

    container_id = fields.Many2one(
        "rigging.component",
        string="Container",
        domain=[("component_type", "=", "container")],
    )

    reserve_id = fields.Many2one(
        "rigging.component",
        string="Reserve",
        domain=[("component_type", "=", "reserve")],
    )

    aad_id = fields.Many2one(
        "rigging.component",
        string="AAD",
        domain=[("component_type", "=", "aad")],
    )

    # -------------------------------------------------
    # CAMBIO DE OWNER → aplicar en componentes montados
    # -------------------------------------------------
    @api.onchange("owner_id")
    def _onchange_owner_id(self):
        for rig in self:
            for comp in [
                rig.canopy_id,
                rig.container_id,
                rig.reserve_id,
                rig.aad_id,
            ]:
                if comp:
                    comp.owner_id = rig.owner_id

    # -------------------------------------------------
    # SINCRONIZAR rig <-> componente.rig_id
    # -------------------------------------------------
    def _sync_components(self):
        """Mantiene rig_id e is_mounted en rigging.component."""
        Component = self.env["rigging.component"]

        for rig in self:
            selected_ids = []

            # comprobar todos los "slots"
            for slot in ["canopy_id", "container_id", "reserve_id", "aad_id"]:
                comp = getattr(rig, slot)
                if comp:
                    selected_ids.append(comp.id)

                    # liberar si estaban en otro rig
                    if comp.rig_id and comp.rig_id != rig:
                        comp.rig_id = False
                        comp.is_mounted = False

                    # asignar al rig actual
                    comp.rig_id = rig.id
                    comp.is_mounted = True
                    if rig.owner_id:
                        comp.owner_id = rig.owner_id

            # componentes huérfanos: tenían rig_id=este rig pero ya no están en slots
            orphans = Component.search([
                ("rig_id", "=", rig.id),
                ("id", "not in", selected_ids),
            ])

            orphans.write({
                "rig_id": False,
                "is_mounted": False,
            })

    @api.model
    def create(self, vals):
        rig = super().create(vals)
        rig._sync_components()
        return rig

    def write(self, vals):
        res = super().write(vals)
        self._sync_components()
        return res

    # ------------------------------------------------------------
    # FILTRO INTELIGENTE PARA LA SELECCIÓN DE RIG DESDE COMPONENT
    # ------------------------------------------------------------
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        domain = list(domain or [])
        ctx = self.env.context or {}

        component_type = ctx.get("component_type")
        current_component_id = ctx.get("current_component_id")

        if component_type:
            field_map = {
                "canopy": "canopy_id",
                "container": "container_id",
                "reserve": "reserve_id",
                "aad": "aad_id",
            }
            f = field_map.get(component_type)
            if f:
                domain += [
                    "|",
                    (f, "=", False),
                    (f, "=", current_component_id),
                ]

        return super(Rig, self).name_search(name, domain, operator, limit)

    # ============================================================
    # 🔹 Helper: obtener todos los componentes montados en este rig
    # ============================================================
    def _get_mounted_components(self):
        """Devuelve todos los componentes montados en este rig."""
        self.ensure_one()
        comps = []
        for slot in ["canopy_id", "container_id", "reserve_id", "aad_id"]:
            c = getattr(self, slot)
            if c:
                comps.append(c.id)
        return self.env["rigging.component"].browse(comps)

    # ============================================================
    # 🔥 Acción genérica: update saltos en TODO el equipo
    # ============================================================
    def action_update_all_jumps(self, aad_jumps_str):
        """
        Actualiza los saltos de TODOS los componentes montados del rig,
        excepto la reserve.

        Fórmula:
            total_jumps += aad_jumps - jumps_on_mount
            jumps_on_mount = aad_jumps
        """
        self.ensure_one()

        # --- validar entrada ---
        if not aad_jumps_str:
            raise UserError("Please enter the AAD jumps.")

        try:
            aad_jumps = int(aad_jumps_str)
        except ValueError:
            raise UserError("AAD jumps must be a number.")

        # --- obtener componentes ---
        components = self._get_mounted_components()

        # --- aplicar lógica ---
        for comp in components:
            if comp.component_type == "reserve":
                continue  # la reserve nunca se toca

            old_mount = comp.jumps_on_mount or 0
            delta = aad_jumps - old_mount

            comp.total_jumps = (comp.total_jumps or 0) + delta
            comp.jumps_on_mount = aad_jumps

        return True