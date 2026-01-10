from odoo import api, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        # Solo si no viene ya un partner por contexto
        if not res.get("partner_id") and self.env.context.get("rigging_default_partner_skdm"):
            partner = self.env["res.partner"].search([("name", "=", "SKDM")], limit=1)
            if partner:
                res["partner_id"] = partner.id

        return res