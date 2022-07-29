from odoo import models, fields, api

class ComponentModel(models.Model):
    _name = 'rigging.model'
    _description = 'Model'

    name = fields.Char()
    manifacturer_id = fields.Many2one( 'rigging.manifacturer' ) 
    components_id = fields.Many2one( 'rigging.components' )
