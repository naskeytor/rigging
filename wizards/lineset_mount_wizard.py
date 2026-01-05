from odoo import models, fields
from odoo.exceptions import UserError


class LinesetMountWizard(models.TransientModel):
    _name = "rigging.lineset.mount.wizard"
    _description = "Mount / Unmount Lineset"

    action_type = fields.Selection(
        [("mount", "Mount"), ("unmount", "Unmount")],
        required=True,
        readonly=True,
    )

    lineset_id = fields.Many2one("rigging.lineset", required=True, readonly=True)

    canopy_id = fields.Many2one(
        "rigging.component",
        string="Canopy",
        domain="[('component_type','=','canopy')]",
        required=True,
    )

    aad_jumps = fields.Integer(string="AAD Jumps", default=0)

    canopy_last_jumps_update = fields.Integer(string="Canopy last jumps update", readonly=True)
    lineset_jumps_on_mount = fields.Integer(string="Lineset jumps on mount", readonly=True)
    lineset_total_jumps = fields.Integer(string="Lineset total jumps", readonly=True)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        lineset = self.env["rigging.lineset"].browse(res.get("lineset_id"))

        if lineset:
            res["lineset_jumps_on_mount"] = lineset.jumps_on_mount
            res["lineset_total_jumps"] = lineset.total_jumps

            if res.get("action_type") == "unmount":
                res["canopy_id"] = lineset.canopy_id.id
                res["canopy_last_jumps_update"] = lineset.canopy_id.last_jumps_update

        return res

    def action_apply(self):
        self.ensure_one()

        if self.aad_jumps < 0:
            raise UserError("AAD Jumps must be positive.")

        lineset = self.lineset_id

        # ---------------- MOUNT ----------------
        if self.action_type == "mount":
            canopy = self.canopy_id

            lineset.canopy_id = canopy.id
            lineset.mounted_on = fields.Datetime.now()

            # ✅ IGUAL QUE DROGUE:
            # baseline de “jumps on mount” viene del total del canopy
            lineset.jumps_on_mount = canopy.total_jumps

            # snapshot para calcular delta al unmount
            lineset.last_jumps_update = canopy.last_jumps_update

        # ---------------- UNMOUNT ----------------
        else:
            canopy = lineset.canopy_id
            baseline = canopy.last_jumps_update or 0
            delta = baseline - (lineset.last_jumps_update or 0)

            if delta < 0:
                raise UserError("AAD jumps cannot be lower than last canopy update.")

            lineset.total_jumps += delta
            lineset.jumps_on_mount = 0
            lineset.canopy_id = False
            lineset.last_jumps_update = 0
            lineset.mounted_on = False

        return {"type": "ir.actions.act_window_close"}