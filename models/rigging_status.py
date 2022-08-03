from odoo import models, fields, api

class Status(models.Model):
    _name = 'rigging.status'
    _description = 'Status'

    name = fields.Char()
    #canopy_id = fields.One2many( 'rigging.canopy', 'status_id' )
