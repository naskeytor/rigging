from odoo import models, fields
from odoo.exceptions import UserError


class DrogueMountWizard(models.TransientModel):
    _name = "rigging.drogue.mount.wizard"
    _description = "Mount / Unmount Drogue"

    drogue_id = fields.Many2one("rigging.drogue", required=True)
    container_id = fields.Many2one(
        "rigging.component",
        domain=[
            ("component_type", "=", "container"),
            ("usage_type", "=", "tandem"),
        ],
    )
    action_type = fields.Selection(
        [("mount", "Mount"), ("unmount", "Unmount")],
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()
        drogue = self.drogue_id

        if self.action_type == "mount":
            if not self.container_id:
                raise UserError("Please select a container.")
            drogue.container_id = self.container_id.id
            drogue.mounted_on = fields.Datetime.now()

        if self.action_type == "unmount":
            drogue.container_id = False
            drogue.mounted_on = False