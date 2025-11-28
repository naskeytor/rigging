from odoo import models, fields, api


class Rig(models.Model):
    _name = "rigging.rig"
    _description = "Rig"
    _order = "number"

    number = fields.Integer(string="Rig Number", required=True)

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
        help="Owner of this rig and its mounted components.",
    )

    canopy_id = fields.Many2one(
        "rigging.component",
        string="Canopy",
        domain=[("component_type", "=", "canopy")],
    )
    container_id = fields.Many2one(
        "rigging.component",
        string="Container",
        domain=[("component_type", "=", "container")],
    )
    reserve_id = fields.Many2one(
        "rigging.component",
        string="Reserve",
        domain=[("component_type", "=", "reserve")],
    )
    aad_id = fields.Many2one(
        "rigging.component",
        string="AAD",
        domain=[("component_type", "=", "aad")],
    )

    # ... tu _sync_components(), create(), write() se quedan igual ...

    # -------- FILTRO PARA RIG_ID EN COMPONENT -----------
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        domain = list(domain or [])
        ctx = self.env.context or {}

        component_type = ctx.get("component_type")
        current_component_id = ctx.get("current_component_id")

        if component_type:
            field_map = {
                "canopy": "canopy_id",
                "container": "container_id",
                "reserve": "reserve_id",
                "aad": "aad_id",
            }
            f = field_map.get(component_type)
            if f:
                # rigs donde ese campo está vacío O tiene este mismo componente
                domain += [
                    "|",
                    (f, "=", False),
                    (f, "=", current_component_id),
                ]

        # llamada correcta a super() en Odoo 19
        return super(Rig, self).name_search(name, domain, operator, limit)