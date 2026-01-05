from odoo import models, fields, api
from odoo.exceptions import UserError


class Lineset(models.Model):
    _name = "rigging.lineset"
    _description = "Lineset"
    _order = "name"

    name = fields.Char(string="Lineset Serial", required=True)

    manufacturer_id = fields.Many2one("rigging.manufacturer", string="Manufacturer")
    model_id = fields.Many2one("rigging.model", string="Model")
    dom = fields.Date(string="DOM")

    # 🔗 MONTAJE EN CANOPY (SOLO POR WIZARD)
    canopy_id = fields.Many2one(
        "rigging.component",
        string="Mounted on Canopy",
        domain=[("component_type", "=", "canopy")],
        readonly=True,  # 🔒 crítico
    )

    mounted_on = fields.Datetime(string="Mounted On", readonly=True)
    is_mounted = fields.Boolean(string="Mounted", compute="_compute_is_mounted", store=True)

    notes = fields.Text(string="Notes")

    jumps_on_mount = fields.Integer(string="Jumps on mount", default=0, readonly=True)
    last_jumps_update = fields.Integer(string="Last jumps update", default=0, readonly=True)
    total_jumps = fields.Integer(string="Total jumps", default=0, readonly=True)

    @api.depends("canopy_id")
    def _compute_is_mounted(self):
        for ls in self:
            ls.is_mounted = bool(ls.canopy_id)

    def action_mount(self):
        self.ensure_one()
        if self.is_mounted:
            raise UserError("This lineset is already mounted.")
        return {
            "type": "ir.actions.act_window",
            "name": "Mount Lineset",
            "res_model": "rigging.lineset.mount.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lineset_id": self.id,
                "default_action_type": "mount",
            },
        }

    def action_unmount(self):
        self.ensure_one()
        if not self.is_mounted:
            raise UserError("This lineset is not mounted.")
        return {
            "type": "ir.actions.act_window",
            "name": "Unmount Lineset",
            "res_model": "rigging.lineset.mount.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lineset_id": self.id,
                "default_action_type": "unmount",
            },
        }