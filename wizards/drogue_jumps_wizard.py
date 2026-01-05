from odoo import models, fields
from odoo.exceptions import UserError


class DrogueJumpsWizard(models.TransientModel):
    _name = "rigging.drogue.jumps.wizard"
    _description = "Drogue Jumps Wizard"

    drogue_id = fields.Many2one("rigging.drogue", required=True, readonly=True)
    container_id = fields.Many2one("rigging.component", string="Container", required=True, readonly=True)

    container_total_jumps = fields.Integer(string="Container total jumps", readonly=True)
    add_jumps = fields.Integer(string="Add jumps", default=0)

    def action_apply(self):
        self.ensure_one()

        if self.add_jumps < 0:
            raise UserError("Add jumps must be 0 or positive.")

        drogue = self.drogue_id

        # suma manual (simple)
        drogue.total_jumps += self.add_jumps
        drogue.last_jumps_update = drogue.total_jumps

        return {"type": "ir.actions.act_window_close"}

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        drogue_id = res.get("drogue_id")
        container_id = res.get("container_id")

        if drogue_id and container_id:
            container = self.env["rigging.component"].browse(container_id)
            res["container_total_jumps"] = container.total_jumps or 0

        return res
