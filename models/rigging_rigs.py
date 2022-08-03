from odoo import models, fields, api

class ComponentModel(models.Model):
    _name = 'rigging.rigs'
    _description = 'Rigs'
   # _inherit = 'rigging.components'

    number = fields.Char()
    status_id = fields.Many2one( 'rigging.status' )
    
    canopy_id = fields.Many2one( 'rigging.canopy' )
    container_id = fields.Many2one( 'rigging.container' )
    reserve_id = fields.Many2one( 'rigging.reserve' )
    aad_id = fields.Many2one( 'rigging.aad' )

    rig_canopy_model = fields.Char( related="canopy_id.model_canopy")
    rig_container_model = fields.Char( related="container_id.model")
    rig_reserve_model = fields.Char( related="reserve_id.model_reserve")
    rig_aad_model = fields.Char( related="aad_id.model")

