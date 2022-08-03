from odoo import models, fields, api

class ComponentModel(models.Model):
    _name = 'rigging.kit'
    _description = 'Type component'
   # _inherit = 'rigging.components'

    name = fields.Char()
    manifacturer_id = fields.Many2one( 'rigging.manifacturer' ) 
    #components_id = fields.Many2one( 'rigging.components' )
