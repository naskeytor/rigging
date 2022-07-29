from odoo import models, fields, api

class Status(models.Model):
    _name = 'rigging.status'
    _description = 'Status'

    name = fields.Char()
    components_id = fields.Many2one( 'rigging.components' )
