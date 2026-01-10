from odoo import models, fields

class RiggingTaskHome(models.Model):
    _name = "rigging.task.home"
    _description = "Rigging Tasks Home"
    _rec_name = "name"

    name = fields.Char(default="Tasks")