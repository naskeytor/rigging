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

    # -------------------------------
    # Botones (tal como los tenías)
    # -------------------------------
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