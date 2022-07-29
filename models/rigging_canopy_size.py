from odoo import models, fields, api

class RiggingCanopySize(models.Model):

    _name = 'rigging.canopy.size'
    _description = 'Canopy size'

    name = fields.Char()
