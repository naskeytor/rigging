from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    rig_count = fields.Integer(string="Rigs", compute="_compute_counts", store=False)
    component_count = fields.Integer(string="Components", compute="_compute_counts", store=False)
    rigging_count = fields.Integer(string="Rigging", compute="_compute_counts", store=False)

    # Listas embebidas (computed O2M “virtual”)
    rig_ids = fields.One2many("rigging.rig", compute="_compute_rig_ids", string="Rigs", readonly=True)
    component_ids = fields.One2many("rigging.component", compute="_compute_component_ids", string="Components", readonly=True)
    rigging_ids = fields.One2many("rigging.rigging", compute="_compute_rigging_ids", string="Rigging Jobs", readonly=True)

    def _compute_counts(self):
        Rig = self.env["rigging.rig"]
        Component = self.env["rigging.component"]
        Rigging = self.env["rigging.rigging"]
        for p in self:
            p.rig_count = Rig.search_count([("owner_id", "=", p.id)])
            p.component_count = Component.search_count([("owner_id", "=", p.id)])
            p.rigging_count = Rigging.search_count([("owner_id", "=", p.id)])

    def _compute_rig_ids(self):
        Rig = self.env["rigging.rig"]
        for p in self:
            p.rig_ids = Rig.search([("owner_id", "=", p.id)])

    def _compute_component_ids(self):
        Component = self.env["rigging.component"]
        for p in self:
            p.component_ids = Component.search([("owner_id", "=", p.id)])

    def _compute_rigging_ids(self):
        Rigging = self.env["rigging.rigging"]
        for p in self:
            p.rigging_ids = Rigging.search([("owner_id", "=", p.id)])

    # ---- Acciones (para abrir listas completas y poder Exportar) ----
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

    def action_open_owner_rigs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Rigs",
            "res_model": "rigging.rig",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {"default_owner_id": self.id},
        }

    def action_open_owner_components(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Components",
            "res_model": "rigging.component",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {"default_owner_id": self.id},
        }