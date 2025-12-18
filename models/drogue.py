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
    total_cycles = fields.Integer(string="Total Cycles")

    # 🔗 MONTAJE EN CONTAINER
    container_id = fields.Many2one(
        "rigging.component",
        string="Mounted on Container",
        domain=[
            ("component_type", "=", "container"),
            ("usage_type", "=", "tandem"),
        ],
    )

    mounted_on = fields.Datetime(string="Mounted On")
    is_mounted = fields.Boolean(string="Mounted", compute="_compute_is_mounted", store=True)

    notes = fields.Text(string="Notes")

    @api.depends("container_id")
    def _compute_is_mounted(self):
        for d in self:
            d.is_mounted = bool(d.container_id)

    def action_mount(self):
        self.ensure_one()
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
