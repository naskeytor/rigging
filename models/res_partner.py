from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    rig_count = fields.Integer(string="Rigs", compute="_compute_rig_count")
    component_count = fields.Integer(string="Components", compute="_compute_component_count")
    rigging_count = fields.Integer(compute="_compute_rigging_count")

    def _compute_rigging_count(self):
        Rigging = self.env["rigging.rigging"]
        for p in self:
            p.rigging_count = Rigging.search_count([("owner_id", "=", p.id)])

    def action_open_owner_rigging(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Rigging",
            "res_model": "rigging.rigging",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {"default_owner_id": self.id},
        }

    def _compute_rig_count(self):
        Rig = self.env["rigging.rig"]
        for partner in self:
            partner.rig_count = Rig.search_count([("owner_id", "=", partner.id)])

    def _compute_component_count(self):
        Component = self.env["rigging.component"]
        for partner in self:
            partner.component_count = Component.search_count([("owner_id", "=", partner.id)])

    def action_open_owner_rigs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Rigs",
            "res_model": "rigging.rig",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {
                "search_default_owner_id": self.id,
                "default_owner_id": self.id,
            },
        }

    def action_open_owner_components(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Components",
            "res_model": "rigging.component",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {
                "search_default_owner_id": self.id,
                "default_owner_id": self.id,
            },
        }