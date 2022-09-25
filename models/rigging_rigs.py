from odoo import models, fields, api

class ComponentModel(models.Model):
    _name = 'rigging.rigs'
    _description = 'Rigs'

    number = fields.Char()
    status_id = fields.Many2one( 'rigging.status' )
    
    canopy_id = fields.Many2one( 'rigging.canopy', domain=[('is_mounted', '=', False )] )
    container_id = fields.Many2one( 'rigging.container', domain=[('is_mounted', '=', False )] )
    reserve_id = fields.Many2one( 'rigging.reserve' , domain=[('is_mounted', '=', False )])
    aad_id = fields.Many2one( 'rigging.aad', domain=[('is_mounted', '=', False )] )

    rig_canopy_model = fields.Char( related="canopy_id.model_canopy", string="Canopy Model" )
    rig_container_model = fields.Char( related="container_id.model", string="Container Model")
    rig_reserve_model = fields.Char( related="reserve_id.model_reserve", string="Reserve Model")
    rig_aad_model = fields.Char( related="aad_id.model", string="AAD Model")
    
    #mounted_canopy = fields.Char( related="canopy_id.is_mounted", string="Canopy", store=True,  readonly= True)

    rigging_id = fields.Many2one( 'rigging.rigging' )  
