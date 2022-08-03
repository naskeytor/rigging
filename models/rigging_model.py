from odoo import models, fields, api

class ComponentModel(models.Model):
    _name = 'rigging.model'
    _description = 'Model'

    name = fields.Char()
    manifacturer_id = fields.Many2one( 'rigging.manifacturer' ) 
    manifacturer = fields.Char( related="manifacturer_id.name", string="Manifacture" )
    model = fields.Char(compute="_model_canopy") 

    @api.depends("name", "manifacturer")
    def _model_canopy(self):
        for record in self:
            record.model = str(record.name) + str(record.manifacturer)

    #canopy_id = fields.One2many( 'rigging.canopy', 'model_id' )

