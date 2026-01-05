from odoo import models, fields, api
from odoo.exceptions import UserError


class Drogue(models.Model):
    _name = "rigging.drogue"
    _description = "Drogue"
    _order = "name"

    name = fields.Char(string="Serial Number", required=True)

    manufacturer_id = fields.Many2one("rigging.manufacturer", string="Manufacturer")
    model_id = fields.Many2one("rigging.model", string="Model")
    dom = fields.Date(string="DOM")

    # 🔗 MONTAJE EN CONTAINER (SOLO POR WIZARD)
    container_id = fields.Many2one(
        "rigging.component",
        string="Mounted on Container",
        domain=[
            ("component_type", "=", "container"),
            ("usage_type", "=", "tandem"),
        ],
        readonly=True,   # 🔒 CRÍTICO
    )

    mounted_on = fields.Datetime(string="Mounted On", readonly=True)

    is_mounted = fields.Boolean(
        string="Mounted",
        compute="_compute_is_mounted",
        store=True,
    )

    notes = fields.Text(string="Notes")

    # JUMPS
    jumps_on_mount = fields.Integer(string="Jumps on mount", default=0, readonly=True)
    last_jumps_update = fields.Integer(string="Last jumps update", default=0, readonly=True)
    total_jumps = fields.Integer(string="Total jumps", default=0, readonly=True)

    @api.depends("container_id")
    def _compute_is_mounted(self):
        for d in self:
            d.is_mounted = bool(d.container_id)

    # -------------------------------------------------
    # BOTONES (SOLO ABREN WIZARD)
    # -------------------------------------------------
    def action_mount(self):
        self.ensure_one()
        if self.is_mounted:
            raise UserError("This drogue is already mounted.")

        return {
            "type": "ir.actions.act_window",
            "name": "Mount Drogue",
            "res_model": "rigging.drogue.mount.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_drogue_id": self.id,
                "default_action_type": "mount",
            },
        }

    def action_unmount(self):
        self.ensure_one()
        if not self.is_mounted:
            raise UserError("This drogue is not mounted.")

        return {
            "type": "ir.actions.act_window",
            "name": "Unmount Drogue",
            "res_model": "rigging.drogue.mount.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_drogue_id": self.id,
                "default_action_type": "unmount",
            },
        }