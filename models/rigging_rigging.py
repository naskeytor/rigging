from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class RiggingJob(models.Model):
    _name = "rigging.rigging"
    _description = "Rigging Job"
    _order = "date desc, id desc"

    name = fields.Char(string="Reference", readonly=True, copy=False)

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        related="component_id.owner_id",
        store=True,
        readonly=True,
    )

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)

    component_id = fields.Many2one(
        "rigging.component",
        string="Component",
        required=True,
    )

    component_type = fields.Selection(
        related="component_id.component_type",
        string="Component Type",
        readonly=True,
    )

    component_usage_type = fields.Selection(
        related="component_id.usage_type",
        string="Component Usage Type",
        readonly=True,
    )

    component_is_mounted = fields.Boolean(
        related="component_id.is_mounted",
        string="Component Mounted",
        readonly=True,
    )

    jumps = fields.Integer(
        string="Jumps",
        help="Current jumps on the equipment at the time of this job.",
    )

    rigging_type = fields.Selection(
        [
            ("inspection_repack", "I + R"),
            ("repair", "Reparation"),
            ("alteration", "Alteration"),
        ],
        string="Rigging Type",
        required=True,
    )

    reline = fields.Boolean(string="Reline")
    drogue_replace = fields.Boolean(string="Drogue Replace")
    killline_replace = fields.Boolean(string="Kill Line Replace")
    inspection_100_jumps = fields.Boolean(string="100 Jumps Inspection")

    comment = fields.Text(string="Comment")
    price = fields.Float(string="Price")

    state = fields.Selection(
        [("pending", "Pending"), ("paid", "Paid")],
        string="State",
        default="pending",
        required=True,
    )

    price_color = fields.Html(
        string="Price",
        compute="_compute_price_color",
        sanitize=False,
        readonly=True,
    )

    @api.depends("price", "state")
    def _compute_price_color(self):
        for rec in self:
            value = rec.price or 0.0
            rec.price_color = (
                f"<span style='color:red;'>{value}</span>"
                if rec.state == "pending"
                else f"<span style='color:green;'>{value}</span>"
            )

    def _sync_lineset_counter(self):
        for rec in self:
            comp = rec.component_id
            if not comp or comp.component_type != 'canopy':
                continue
            if rec.reline:
                comp.lineset_jumps_frozen = 0
                comp.lineset_ref_jumps = comp.last_jumps_update

    def _sync_tandem_counters(self):
        for rec in self:
            comp = rec.component_id
            if not comp:
                continue

            if comp.component_type == 'container':
                if rec.drogue_replace:
                    comp.drogue_jumps_frozen = 0
                    comp.drogue_ref_jumps = comp.last_jumps_update
                if rec.killline_replace:
                    comp.killline_jumps_frozen = 0
                    comp.killline_ref_jumps = comp.last_jumps_update
                if rec.inspection_100_jumps:
                    comp.inspection_100_jumps_frozen = 0
                    comp.inspection_100_ref_jumps = comp.last_jumps_update

            if rec.inspection_100_jumps and comp.component_type == 'reserve':
                if comp.rig_id and comp.rig_id.container_id:
                    container = comp.rig_id.container_id
                    container.inspection_100_jumps_frozen = 0
                    container.inspection_100_ref_jumps = container.last_jumps_update

    # ------------------------------------------------------------
    # 🔧 Helper: sincronizar last_repack en la reserve
    # ------------------------------------------------------------
    def _sync_last_repack(self):
        for rec in self:
            comp = rec.component_id
            if (
                    rec.rigging_type == "inspection_repack"
                    and comp
                    and comp.component_type == "reserve"
            ):
                comp.write({"last_repack": rec.date or fields.Date.context_today(rec)})

    # ------------------------------------------------------------
    # 🔧 Helper: propagar jumps al rig del componente
    # ------------------------------------------------------------
    def _update_rig_jumps(self):
        for rec in self:
            comp = rec.component_id
            if not rec.jumps or not comp:
                continue
            if comp.rig_id:
                comp.rig_id.action_update_all_jumps(str(rec.jumps))
            elif comp.component_type in ('container', 'canopy'):
                # Component off rig: update last_jumps_update so sync counters
                # capture the correct reference on reset.
                comp.last_jumps_update = rec.jumps

    # ------------------------------------------------------------
    # 🔧 UI: drogue replace implica killline replace (jumps on killline -> 0)
    # ------------------------------------------------------------
    @api.onchange("drogue_replace")
    def _onchange_drogue_replace(self):
        for rec in self:
            if rec.drogue_replace:
                rec.killline_replace = True

    # ------------------------------------------------------------
    # 🔧 I+R en un rig Tandem implica 100 Jumps Inspection
    # ------------------------------------------------------------
    @api.onchange("rigging_type", "component_id")
    def _onchange_inspection_100_jumps(self):
        for rec in self:
            if rec._is_tandem_ir():
                rec.inspection_100_jumps = True

    def _is_tandem_ir(self):
        self.ensure_one()
        return (
            self.rigging_type == "inspection_repack"
            and self.component_id
            and self.component_id.rig_id
            and self.component_id.rig_id.usage_type == "tandem"
        )

    def _apply_100_jumps_inspection_rule(self):
        for rec in self:
            if rec._is_tandem_ir() and not rec.inspection_100_jumps:
                rec.inspection_100_jumps = True

    # ------------------------------------------------------------
    # ✅ UI: filtra + valida inmediatamente
    # ------------------------------------------------------------
    @api.onchange("rigging_type", "component_id")
    def _onchange_ir_requirements(self):
        # dominio dinámico para el campo component_id
        for rec in self:
            domain = [("component_type", "=", "reserve")] if rec.rigging_type == "inspection_repack" else []
            result = {"domain": {"component_id": domain}}

            if not rec.component_id:
                return result

            if rec.rigging_type == "inspection_repack":
                comp = rec.component_id

                if comp.component_type != "reserve":
                    rec.component_id = False
                    raise UserError("I + R can only be done on a Reserve.")

                if not comp.rig_id:
                    rec.component_id = False
                    raise UserError("Reserve must be mounted on a rig.")

                rig = comp.rig_id
                if not rig.container_id:
                    raise UserError("Rig must have a Container mounted for I + R.")
                if not rig.aad_id and rig.usage_type != "pilot":
                    raise UserError("Rig must have an AAD mounted for I + R.")

            return result

    # ------------------------------------------------------------
    # ✅ Backend: reglas reales (import/API)
    # ------------------------------------------------------------
    @api.constrains("rigging_type", "component_id")
    def _check_ir_requirements(self):
        for rec in self:
            if rec.rigging_type != "inspection_repack":
                continue

            comp = rec.component_id
            if not comp:
                continue

            if comp.component_type != "reserve":
                raise ValidationError("I + R can only be done on a Reserve.")

            if not comp.rig_id:
                raise ValidationError("Reserve must be mounted on a rig.")

            rig = comp.rig_id
            if not rig.container_id:
                raise ValidationError("Rig must have a Container mounted for I + R.")
            if not rig.aad_id and rig.usage_type != "pilot":
                raise ValidationError("Rig must have an AAD mounted for I + R.")

    # ------------------------------------------------------------
    # ✅ Backend: create/write robustos (multi)
    # ------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code("rigging.rigging") or "RIG-0000"
            if vals.get("drogue_replace"):
                vals["killline_replace"] = True

        recs = super().create(vals_list)
        recs._apply_100_jumps_inspection_rule()
        recs._sync_last_repack()
        recs._update_rig_jumps()
        recs._sync_tandem_counters()
        recs._sync_lineset_counter()
        return recs

    def write(self, vals):
        if vals.get("drogue_replace"):
            vals["killline_replace"] = True
        res = super().write(vals)
        if any(k in vals for k in ("rigging_type", "component_id")):
            self._apply_100_jumps_inspection_rule()
        if any(k in vals for k in ("rigging_type", "component_id", "date")):
            self._sync_last_repack()
        if "jumps" in vals:
            self._update_rig_jumps()
        if any(k in vals for k in ("drogue_replace", "killline_replace", "inspection_100_jumps", "component_id")):
            self._sync_tandem_counters()
        if any(k in vals for k in ("reline", "component_id")):
            self._sync_lineset_counter()
        return res
