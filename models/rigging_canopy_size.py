from odoo import models, fields, api

class RiggingCanopySize(models.Model):

    _name = 'rigging.canopy.size'
    _description = 'Canopy size'

    name = fields.Char()
    # canopy_id = fields.One2many( 'rigging.canopy', 'size_id' )
