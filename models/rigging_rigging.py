from odoo import models, fields, api

class RiggingJob(models.Model):
    _name = "rigging.rigging"
    _description = "Rigging Job"
    _order = "date desc, id desc"

    name = fields.Char(
        string="Reference",
        readonly=True,
        copy=False,
    )

    owner_id = fields.Many2one("res.partner", string="Owner")
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    component_id = fields.Many2one("rigging.component", string="Component", required=True)
    rigging_type = fields.Selection(
        [
            ("inspection_repack", "I + R"),
            ("repair", "Reparation"),
            ("alteration", "Alteration"),
        ],
        string="Rigging Type",
        required=True,
    )
    comment = fields.Text(string="Comment")
    price = fields.Float(string="Price")

    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("paid", "Paid"),
        ],
        string="State",
        default="pending",
        required=True,
    )

    price_color = fields.Html(
        string="Price",
        compute="_compute_price_color",
        sanitize=False,
        readonly=True,
    )

    @api.depends("price", "state")
    def _compute_price_color(self):
        for rec in self:
            value = rec.price or 0.0
            if rec.state == "pending":
                rec.price_color = f"<span style='color:red;'>{value}</span>"
            else:
                rec.price_color = f"<span style='color:green;'>{value}</span>"

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if not vals.get("name"):
                count = self.search_count([]) + 1
                vals["name"] = f"RIG-{count:04d}"

        return super().create(vals_list)