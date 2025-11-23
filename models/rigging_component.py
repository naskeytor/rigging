from odoo import models, fields


class Component(models.Model):
    _name = "rigging.component"
    _description = "Component"

    name = fields.Char(string="Serial Number", required=True)

    component_type = fields.Selection(
        [
            ("canopy", "Canopy"),
            ("container", "Container"),
            ("reserve", "Reserve"),
            ("aad", "AAD"),
        ],
        string="Type",
        required=True,
    )

    manufacturer_id = fields.Many2one(
        "rigging.manufacturer",
        string="Manufacturer",
    )

    model_id = fields.Many2one(
        "rigging.model",
        string="Model",
    )

    size_id = fields.Many2one(
        "rigging.size",
        string="Size",
    )

    dom = fields.Date(string="DOM")

    jumps_on_mount = fields.Integer(string="Jumps on mount")
    total_jumps = fields.Integer(string="Total jumps")

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        help="Owner of this component",
    )

    # 👇 NUEVO: rig al que está montado
    rig_id = fields.Many2one(
        "rigging.rig",
        string="Rig",
        help="Rig where this component is mounted.",
    )

    is_mounted = fields.Boolean(
        string="Mounted",
        default=False,
    )

    rigging_ids = fields.One2many(
        "rigging.rigging",
        "component_id",
        string="Rigging History",
    )