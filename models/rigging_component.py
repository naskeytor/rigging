from odoo import models, fields, api
from odoo.exceptions import UserError


class Component(models.Model):
    _name = "rigging.component"
    _description = "Component"
    _order = "name"

    name = fields.Char(string="Serial Number", required=True)

    component_type = fields.Selection(
        [
            ("canopy", "Canopy"),
            ("container", "Container"),
            ("reserve", "Reserve"),
            ("aad", "AAD"),
        ],
        string="Type",
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
        help="Defines if this component is for Sport, Tandem, or Pilot rigs.",
    )

    manufacturer_id = fields.Many2one("rigging.manufacturer", string="Manufacturer")
    model_id = fields.Many2one("rigging.model", string="Model")
    size_id = fields.Many2one("rigging.size", string="Size")
    dom = fields.Date(string="DOM")

    jumps_on_mount = fields.Integer(string="Jumps on mount")
    last_jumps_update = fields.Integer(string="Last AAD Jumps Update")
    total_jumps = fields.Integer(string="Total jumps")

    has_reline = fields.Boolean(
        string="Has Reline",
        compute="_compute_jumps_on_lineset",
    )
    jumps_on_lineset = fields.Integer(
        string="Jumps on Lineset",
        compute="_compute_jumps_on_lineset",
        help="Jumps done on the current lineset since the last reline.",
    )

    has_drogue_replace = fields.Boolean(
        string="Has Drogue Replace",
        compute="_compute_jumps_on_drogue",
    )
    jumps_on_drogue = fields.Integer(
        string="Jumps on Drogue",
        compute="_compute_jumps_on_drogue",
        help="Jumps done on the current drogue since the last drogue replace.",
    )

    has_killline_replace = fields.Boolean(
        string="Has Kill Line Replace",
        compute="_compute_jumps_on_killline",
    )
    jumps_on_killline = fields.Integer(
        string="Jumps on Kill Line",
        compute="_compute_jumps_on_killline",
        help="Jumps done on the current kill line since the last kill line replace.",
    )

    has_100_jumps_inspection = fields.Boolean(
        string="Has 100 Jumps Inspection",
        compute="_compute_jumps_on_100_inspection",
    )
    jumps_on_100_inspection = fields.Integer(
        string="Jumps Since Last 100 Jumps Inspection",
        compute="_compute_jumps_on_100_inspection",
        help="Jumps done since the last 100 jumps inspection.",
    )

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        help="Owner of this component",
    )

    # 👇 SIN domain en el campo
    rig_id = fields.Many2one(
        "rigging.rig",
        string="Rig",
        help="Rig where this component is mounted.",
    )

    is_mounted = fields.Boolean(string="Mounted", default=False)

    rigging_ids = fields.One2many(
        "rigging.rigging",
        "component_id",
        string="Rigging History",
    )

    drogue_ids = fields.One2many(
        "rigging.drogue",
        "container_id",
        string="Drogues",
    )

    lineset_ids = fields.One2many(
        "rigging.lineset",
        "canopy_id",
        string="Lineset",
    )

    last_repack = fields.Date(
        string="Last Repack",
        help="Last reserve repack date (auto-set by I+R rigging jobs).",
    )

    @api.depends("rigging_ids.reline", "rigging_ids.jumps", "rigging_ids.date", "last_jumps_update")
    def _compute_jumps_on_lineset(self):
        for comp in self:
            reline_jobs = comp.rigging_ids.filtered("reline")
            if reline_jobs:
                last_reline = max(reline_jobs, key=lambda r: r.date)
                comp.has_reline = True
                comp.jumps_on_lineset = (comp.last_jumps_update or 0) - (last_reline.jumps or 0)
            else:
                comp.has_reline = False
                comp.jumps_on_lineset = 0

    @api.depends("rigging_ids.drogue_replace", "rigging_ids.jumps", "rigging_ids.date", "last_jumps_update")
    def _compute_jumps_on_drogue(self):
        for comp in self:
            drogue_jobs = comp.rigging_ids.filtered("drogue_replace")
            if drogue_jobs:
                last_drogue = max(drogue_jobs, key=lambda r: r.date)
                comp.has_drogue_replace = True
                comp.jumps_on_drogue = (comp.last_jumps_update or 0) - (last_drogue.jumps or 0)
            else:
                comp.has_drogue_replace = False
                comp.jumps_on_drogue = 0

    @api.depends("rigging_ids.killline_replace", "rigging_ids.jumps", "rigging_ids.date", "last_jumps_update")
    def _compute_jumps_on_killline(self):
        for comp in self:
            killline_jobs = comp.rigging_ids.filtered("killline_replace")
            if killline_jobs:
                last_killline = max(killline_jobs, key=lambda r: r.date)
                comp.has_killline_replace = True
                comp.jumps_on_killline = (comp.last_jumps_update or 0) - (last_killline.jumps or 0)
            else:
                comp.has_killline_replace = False
                comp.jumps_on_killline = 0

    @api.depends(
        "rigging_ids.inspection_100_jumps", "rigging_ids.jumps", "rigging_ids.date", "last_jumps_update",
        "rig_id.reserve_id.rigging_ids.inspection_100_jumps",
        "rig_id.reserve_id.rigging_ids.jumps",
        "rig_id.reserve_id.rigging_ids.date",
    )
    def _compute_jumps_on_100_inspection(self):
        for comp in self:
            inspection_jobs = comp.rigging_ids.filtered("inspection_100_jumps")
            if comp.rig_id and comp.rig_id.reserve_id:
                inspection_jobs |= comp.rig_id.reserve_id.rigging_ids.filtered("inspection_100_jumps")
            if inspection_jobs:
                last_inspection = max(inspection_jobs, key=lambda r: (r.date, r.id))
                comp.has_100_jumps_inspection = True
                # I+R jobs on the reserve don't always carry the rig's jump count,
                # so fall back to the container's current count to read as 0.
                baseline_jumps = last_inspection.jumps or comp.last_jumps_update or 0
                comp.jumps_on_100_inspection = (comp.last_jumps_update or 0) - baseline_jumps
            else:
                comp.has_100_jumps_inspection = False
                comp.jumps_on_100_inspection = 0

    # -------------------------------
    # Botones (tal como los tenías)
    # -------------------------------
    def action_refresh(self):
        """Recarga el formulario para reflejar saltos actualizados desde un rigging job."""
        return True

    def action_open_mount_wizard(self):
        self.ensure_one()
        if not self.rig_id:
            raise UserError("Please select a rig before mounting the component.")
        return {
            "type": "ir.actions.act_window",
            "name": "Mount Component",
            "res_model": "rigging.aad.jumps.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_component_id": self.id,
                "default_rig_id": self.rig_id.id,
                "default_action_type": "mount",
            },
        }

    def action_open_unmount_wizard(self):
        self.ensure_one()
        if not self.rig_id:
            raise UserError("This component is not mounted on any rig.")
        return {
            "type": "ir.actions.act_window",
            "name": "Unmount Component",
            "res_model": "rigging.aad.jumps.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_component_id": self.id,
                "default_rig_id": self.rig_id.id,
                "default_action_type": "unmount",
            },
        }

    def name_get(self):
        res = []
        for rec in self:
            model = rec.model_id.display_name if rec.model_id else ""
            size = rec.size_id.display_name if rec.size_id else ""

            # AAD => solo modelo
            if rec.component_type == "aad":
                label = model

            # canopy/container/reserve => modelo-size (si no hay size => solo modelo)
            elif rec.component_type in ("canopy", "container", "reserve"):
                label = model
                if size:
                    label = f"{model}-{size}" if model else size

            else:
                label = model or rec.name or ""

            # fallback final
            if not label:
                label = rec.name or ""

            res.append((rec.id, label))
        return res

    # ---------------------------------------------------
    # Validar que no se repita tipo en el mismo rig
    # ---------------------------------------------------
    @api.onchange("rig_id")
    def _onchange_rig_id(self):
        for comp in self:
            rig = comp.rig_id
            if not rig or not comp.component_type:
                continue

            # según el tipo miramos el campo del rig
            if comp.component_type == "canopy" and rig.canopy_id and rig.canopy_id != comp:
                comp.rig_id = False
                raise UserError("This rig already has a canopy mounted.")

            if comp.component_type == "container" and rig.container_id and rig.container_id != comp:
                comp.rig_id = False
                raise UserError("This rig already has a container mounted.")

            if comp.component_type == "reserve" and rig.reserve_id and rig.reserve_id != comp:
                comp.rig_id = False
                raise UserError("This rig already has a reserve mounted.")

            if comp.component_type == "aad" and rig.aad_id and rig.aad_id != comp:
                comp.rig_id = False
                raise UserError("This rig already has an AAD mounted.")
