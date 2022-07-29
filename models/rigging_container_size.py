from odoo import models, fields, api

class RiggingContainerSize(models.Model):
    _name = 'rigging.container.size'
    _description = 'Container Size'

    name = fields.Char()
