from odoo import models, fields, api

class Type(models.Model):
    _name = 'rigging.type'
    _description = 'Type'

    name = fields.Char()
    components_id = fields.Many2one( 'rigging.components' )
