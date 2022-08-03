from odoo import models, fields, api

class RiggingContainerSize(models.Model):
    _name = 'rigging.container.size'
    _description = 'Container Size'

    name = fields.Char()
    #container_id = fields.One2many( 'rigging.container', 'size_id' )
