from odoo import models, fields


class Size(models.Model):
    _name = "rigging.size"
    _description = "Size"


    name = fields.Char(string="Size")



