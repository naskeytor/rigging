from odoo import models, fields, api
from odoo.exceptions import UserError


class Rig(models.Model):
    _name = "rigging.rig"
    _description = "Rig"
    _order = "sequence, number"

    sequence = fields.Integer(string="Sequence", default=10)

    # ------------------------------------------
    # CAMPOS PRINCIPALES
    # ------------------------------------------
    number = fields.Char(string="Rig Number", required=True)

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

    service_state = fields.Selection(
        [
            ("in_service", "In Service"),
            ("out_of_service", "Out of Service"),
        ],
        string="Status",
        default="in_service",
        required=True,
    )

    usage_type = fields.Selection(
        [
            ("sport", "Sport"),
            ("tandem", "Tandem"),
            ("pilot", "Pilot"),
        ],
        string="Discipline",
        default="sport",
        required=True,
        help="Defines if this rig is for Sport, Tandem, or Pilot.",
    )

    reserve_last_repack = fields.Date(
        string="Last Repack",
        compute="_compute_reserve_last_repack",
        store=True,
        readonly=True,
    )

    @api.depends("reserve_id", "reserve_id.last_repack")
    def _compute_reserve_last_repack(self):
        for rig in self:
            rig.reserve_last_repack = (
                rig.reserve_id.last_repack if rig.reserve_id else False
            )

    last_jumps_update_date = fields.Date(
        string="Last Jumps Update",
        compute="_compute_last_jumps_update_date",
        store=True,
        readonly=True,
    )

    @api.depends("canopy_id.last_jumps_update_date", "container_id.last_jumps_update_date")
    def _compute_last_jumps_update_date(self):
        for rig in self:
            rig.last_jumps_update_date = (
                rig.canopy_id.last_jumps_update_date
                or rig.container_id.last_jumps_update_date
                or False
            )

    last_loop_adjust = fields.Date(
        string="Last Loop Adjust",
        compute="_compute_last_loop_adjust",
        store=True,
        readonly=True,
    )

    @api.depends("container_id.last_loop_adjust")
    def _compute_last_loop_adjust(self):
        for rig in self:
            rig.last_loop_adjust = rig.container_id.last_loop_adjust or False

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
    # DISPLAY NAME
    # -------------------------------------------------
    def _compute_display_name(self):
        for rig in self:
            owner = rig.owner_id.name or ""
            number = rig.number or ""
            rig.display_name = f"{owner} {number}".strip() if owner else number

    # -------------------------------------------------
    # ESTADO DE SERVICIO
    # -------------------------------------------------
    def _check_service_state(self):
        for rig in self:
            incomplete = not rig.canopy_id or not rig.container_id or not rig.reserve_id or not rig.aad_id
            if incomplete and rig.service_state == "in_service":
                rig.service_state = "out_of_service"

    def action_set_in_service(self):
        for rig in self:
            if not rig.canopy_id or not rig.container_id or not rig.reserve_id or not rig.aad_id:
                raise UserError("Rig must have Canopy, Container, Reserve and AAD mounted to be In Service.")
            rig.service_state = "in_service"

    def action_set_out_of_service(self):
        self.service_state = "out_of_service"

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

        self._check_service_state()

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
        usage_type = ctx.get("usage_type")

        # ✅ disciplina SOLO si no es AAD
        if usage_type and component_type != "aad":
            domain += [("usage_type", "=", usage_type)]

        # ✅ tu filtro existente: que el slot esté libre o sea el mismo componente
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

        return super().name_search(name, domain, operator, limit)

    # ============================================================
    # 🔥 Acción genérica: update saltos en TODO el equipo
    # ============================================================
    def action_update_all_jumps(self, aad_jumps_str, date=None):
        """
        Actualiza los saltos de TODOS los componentes montados del rig,
        excepto la reserve.

        Fórmula (no AAD):
            last_jumps_update == 0 -> last_jumps_update = jumps_on_mount
            delta = aad_jumps - last_jumps_update
            last_jumps_update = aad_jumps
            total_jumps += delta

        AAD:
            total_jumps = aad_jumps
        """
        self.ensure_one()
        date = date or fields.Date.context_today(self)

        # --- validar entrada ---
        if not aad_jumps_str:
            raise UserError("Please enter the AAD jumps.")

        try:
            aad_jumps = int(aad_jumps_str)
        except ValueError:
            raise UserError("AAD jumps must be a number.")

        if aad_jumps < 0:
            raise UserError("AAD jumps cannot be negative.")

        # --- obtener componentes ---
        components = self.env["rigging.component"].search([
            ("rig_id", "=", self.id),
            ("component_type", "!=", "reserve"),
        ])

        # --- aplicar lógica ---
        for comp in components:
            if comp.component_type != "aad":
                if comp.last_jumps_update == 0:
                    comp.last_jumps_update = comp.jumps_on_mount
                delta = aad_jumps - (comp.last_jumps_update or 0)
                comp.last_jumps_update = aad_jumps
                comp.last_jumps_update_date = date
                comp.total_jumps = (comp.total_jumps or 0) + delta
            else:
                comp.total_jumps = aad_jumps

        return True
