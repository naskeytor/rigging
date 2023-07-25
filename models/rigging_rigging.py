from odoo import models, fields, api

class RiggingRigging(models.Model):
    _name = 'rigging.rigging'
    _description = "Rigging Management"
    #_rec_name = "date"

    #name = fields.Char()
    name = fields.Many2one("res.partner", string="Partner")
    date = fields.Date('Date')


    rigging_type = fields.Selection(
        string = "Type",
        selection = [
            ('packing', 'I + R'),
            ('reparation', 'Reparation'),
            ('alternation', 'Alternation')
        ]
    )
    """rigging_component = fields.Selection(
        string = "Component",
        selection = [
            ('rig', 'Rig'),
            ('container', 'Container'),
            ('canopy', 'Canopy'),
            ('reserve', 'Reserve'),
            ('aad', 'Aad')
        ]
    )"""

    comp_id = fields.Many2one('rigging.comp')
    compt_id = fields.Many2one('rigging.compt')



    #component_sn = fields.Char(related='comp_id.name', string='Serial Number')
    """container_id = fields.Many2one('rigging.container')
    reserve_id = fields.Many2one('rigging.reserve')
    aad_id = fields.Many2one('rigging.aad')"""
    rig_id = fields.Many2one('rigging.rigs')
    description = fields.Char()

    @api.onchange('compt_id')
    def on_change_component(self):
        for rec in self:
            return {'domain': {'comp_id': [('compt_id', '=', rec.compt_id.id)]}}

        """if self.rigging_component:
            domain = [('rigging_component', '=', self.rigging_component)]
            return {'domain': {'comp_id': domain}}
        else:
            return {'domain': {'comp_id': []}}"""




    """serial_canopy = fields.Char(related='canopy_id.name', string='Canopy number')
    serial_container = fields.Char(related='container_id.name', string='Container number')
    serial_reserve = fields.Char(related='reserve_id.name', string='Reserve number')
    serial_aad = fields.Char(related='aad_id.name', string='AAD number')
    serial_rig = fields.Char(related='rig_id.name', string='Rig number')"""



    """rig_number = fields.Char( related = 'rig_id.number' )
    canopy_sn = fields.Char( related = 'canopy_id.name' )
    container_sn = fields.Char( related = 'container_id.name' )
    reserve_sn = fields.Char( related = 'reserve_id.name' )
    aad_sn = fields.Char( related = 'aad_id.name' )"""
