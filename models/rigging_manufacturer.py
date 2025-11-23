from odoo import models, fields


class Manufacturer(models.Model):
    _name = "rigging.manufacturer"
    _description = "Manufacturer"

    name = fields.Char(string="Name", required=True)
