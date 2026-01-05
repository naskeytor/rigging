from odoo import models, fields
from odoo.exceptions import UserError


class DrogueMountWizard(models.TransientModel):
    _name = "rigging.drogue.mount.wizard"
    _description = "Mount / Unmount Drogue"

    action_type = fields.Selection(
        [("mount", "Mount"), ("unmount", "Unmount")],
        required=True,
        readonly=True,
    )

    drogue_id = fields.Many2one("rigging.drogue", required=True, readonly=True)

    container_id = fields.Many2one(
        "rigging.component",
        string="Container",
        domain="[('component_type','=','container'), ('usage_type','=','tandem')]",
        required=True,
    )

    aad_jumps = fields.Integer(string="AAD Jumps", default=0)

    container_last_jumps_update = fields.Integer(string="Container last jumps update", readonly=True)
    drogue_jumps_on_mount = fields.Integer(string="Drogue jumps on mount", readonly=True)
    drogue_total_jumps = fields.Integer(string="Drogue total jumps", readonly=True)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        drogue = self.env["rigging.drogue"].browse(res.get("drogue_id"))

        if drogue:
            res["drogue_jumps_on_mount"] = drogue.jumps_on_mount
            res["drogue_total_jumps"] = drogue.total_jumps

            if res.get("action_type") == "unmount":
                res["container_id"] = drogue.container_id.id
                res["container_last_jumps_update"] = drogue.container_id.last_jumps_update

        return res

    def action_apply(self):
        self.ensure_one()

        if self.aad_jumps < 0:
            raise UserError("AAD Jumps must be positive.")

        drogue = self.drogue_id


        # ---------------- MOUNT ----------------
        if self.action_type == "mount":
            container = self.container_id

            drogue.container_id = container.id
            drogue.mounted_on = fields.Datetime.now()
            drogue.jumps_on_mount = container.total_jumps

            drogue.last_jumps_update = container.last_jumps_update

        # ---------------- UNMOUNT ----------------
        else:
            container = drogue.container_id
            baseline = container.last_jumps_update or 0
            delta = baseline - drogue.last_jumps_update

            if delta < 0:
                raise UserError("AAD jumps cannot be lower than last container update.")

            drogue.total_jumps += delta
            drogue.jumps_on_mount = 0
            drogue.container_id = False
            drogue.last_jumps_update = 0
            drogue.mounted_on = False

        return {"type": "ir.actions.act_window_close"}