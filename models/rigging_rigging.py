from odoo import models, fields, api

class RiggingRigging(models.Model):
    _name = 'rigging.rigging'
    _description = "Rigging Management"
    #_rec_name = "day"

    name = fields.Char()
    date = fields.Date()
    rigging_type = fields.Selection(
        string = "Type",
        selection = [
            ('packing', 'I + R'),
            ('reparation', 'Reparation'),
            ('alternation', 'Alternation')
        ]
    )
    rigging_component = fields.Selection(
        string = "Component",
        selection = [
            ('rig', 'Rig'),
            ('container', 'Container'),
            ('canopy', 'Canopy'),
            ('reserve', 'Reserve'),
            ('aad', 'Aad')
        ]
    )
    canopy_id = fields.Many2one('rigging.canopy')
    container_id = fields.Many2one('rigging.container')
    reserve_id = fields.Many2one('rigging.reserve')
    aad_id = fields.Many2one('rigging.aad')
    rig_id = fields.Many2one('rigging.rigs')


    """rig_number = fields.Char( related = 'rig_id.number' )
    canopy_sn = fields.Char( related = 'canopy_id.name' )
    container_sn = fields.Char( related = 'container_id.name' )
    reserve_sn = fields.Char( related = 'reserve_id.name' )
    aad_sn = fields.Char( related = 'aad_id.name' )"""
