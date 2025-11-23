from odoo import models, fields


class RiggingModel(models.Model):
    _name = "rigging.model"
    _description = "Rigging Model"

    name = fields.Char(string="Model", required=True)

