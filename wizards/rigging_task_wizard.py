from odoo import api, fields, models
from odoo.exceptions import UserError

class RiggingTaskWizard(models.TransientModel):
    _name = "rigging.task.wizard"
    _description = "Rigging Task Wizard"

    customer_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    rig_id = fields.Many2one(
        "rigging.rig",
        string="Rig",
        required=True,
        domain="[('owner_id','=',customer_id)]",
    )

    component_type = fields.Selection(
        [
            ("canopy", "Canopy"),
            ("container", "Container"),
            ("aad", "AAD"),
            ("reserve", "Reserve"),
        ],
        string="Component",
        required=True,
    )

    issue = fields.Text(string="Issue / Description", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        # Cliente por defecto: SKDM (si existe)
        skdm = self.env["res.partner"].search([("name", "=", "SKDM")], limit=1)
        if skdm:
            res["customer_id"] = skdm.id

        return res

    def action_submit(self):
        self.ensure_one()

        project = self.env["project.project"].search([("name", "=", "Work Flow")], limit=1)
        if not project:
            raise UserError(("Project 'Work Flow' not found. Create it first in Project app."))

        vals = {
            "name": f"Rig - {self.rig_id.number} {dict(self._fields['component_type'].selection).get(self.component_type)}",
            "project_id": project.id,
            "partner_id": self.customer_id.id if self.customer_id else False,
            "description": (
                f"<p><b>Customer:</b> {self.customer_id.name if self.customer_id else ''}</p>"
                f"<p><b>Rig:</b> {self.rig_id.number}</p>"
                f"<p><b>Component:</b> {dict(self._fields['component_type'].selection).get(self.component_type)}</p>"
                f"<p><b>Issue:</b><br/>{(self.issue or '').replace(chr(10), '<br/>')}</p>"
            ),
            # Odoo moderno: asignados = user_ids (m2m)
            "user_ids": [(6, 0, [self.env.user.id])],
        }

        task = self.env["project.task"].create(vals)

        # Abre el task creado
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "res_id": task.id,
            "view_mode": "form",
            "target": "current",
        }