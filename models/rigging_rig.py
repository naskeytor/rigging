from odoo import models, fields, api


class Rig(models.Model):
    _name = "rigging.rig"
    _description = "Rig"

    # Número de rig (ej. 123, 45, etc.)
    number = fields.Integer(string="Rig Number", required=True)

    # Owner del rig (y de sus componentes)
    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        help="Owner of this rig and its mounted components.",
    )

    # Componentes montados
    canopy_id = fields.Many2one(
        "rigging.component",
        string="Canopy",
        domain=[
            ("component_type", "=", "canopy"),
            ("rig_id", "=", False),  # solo los no montados
        ],
    )

    container_id = fields.Many2one(
        "rigging.component",
        string="Container",
        domain=[
            ("component_type", "=", "container"),
            ("rig_id", "=", False),
        ],
    )

    reserve_id = fields.Many2one(
        "rigging.component",
        string="Reserve",
        domain=[
            ("component_type", "=", "reserve"),
            ("rig_id", "=", False),
        ],
    )

    aad_id = fields.Many2one(
        "rigging.component",
        string="AAD",
        domain=[
            ("component_type", "=", "aad"),
            ("rig_id", "=", False),
        ],
    )

    # -------------------------------------------------
    # Propagación de owner a los componentes montados
    # -------------------------------------------------
    @api.onchange("owner_id")
    def _onchange_owner_id(self):
        """Cuando se cambia el owner del rig, aplicar también a los componentes montados."""
        for rig in self:
            for comp in [rig.canopy_id, rig.container_id, rig.reserve_id, rig.aad_id]:
                if comp:
                    comp.owner_id = rig.owner_id

    # -------------------------------------------------
    # Montaje de componentes al rig (onchange)
    # -------------------------------------------------
    @api.onchange("canopy_id")
    def _onchange_canopy_id(self):
        for rig in self:
            # liberar canopy anterior
            if rig._origin and rig._origin.canopy_id and rig._origin.canopy_id != rig.canopy_id:
                prev = rig._origin.canopy_id
                prev.rig_id = False
                prev.is_mounted = False

            if rig.canopy_id:
                rig.canopy_id.rig_id = rig
                rig.canopy_id.is_mounted = True
                if rig.owner_id:
                    rig.canopy_id.owner_id = rig.owner_id

    @api.onchange("container_id")
    def _onchange_container_id(self):
        for rig in self:
            if rig._origin and rig._origin.container_id and rig._origin.container_id != rig.container_id:
                prev = rig._origin.container_id
                prev.rig_id = False
                prev.is_mounted = False

            if rig.container_id:
                rig.container_id.rig_id = rig
                rig.container_id.is_mounted = True
                if rig.owner_id:
                    rig.container_id.owner_id = rig.owner_id

    @api.onchange("reserve_id")
    def _onchange_reserve_id(self):
        for rig in self:
            if rig._origin and rig._origin.reserve_id and rig._origin.reserve_id != rig.reserve_id:
                prev = rig._origin.reserve_id
                prev.rig_id = False
                prev.is_mounted = False

            if rig.reserve_id:
                rig.reserve_id.rig_id = rig
                rig.reserve_id.is_mounted = True
                if rig.owner_id:
                    rig.reserve_id.owner_id = rig.owner_id

    @api.onchange("aad_id")
    def _onchange_aad_id(self):
        for rig in self:
            if rig._origin and rig._origin.aad_id and rig._origin.aad_id != rig.aad_id:
                prev = rig._origin.aad_id
                prev.rig_id = False
                prev.is_mounted = False

            if rig.aad_id:
                rig.aad_id.rig_id = rig
                rig.aad_id.is_mounted = True
                if rig.owner_id:
                    rig.aad_id.owner_id = rig.owner_id