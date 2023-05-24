from odoo import models, fields, api

class RigComponents(models.Model):
    _name = 'rigging.components'
    _description = 'Rig Components'

    name = fields.Char(string="Name")
    model_id = fields.Many2one('rigging.model', string="Model_ID")
    model = fields.Char(related="model_id.name", string="Model")
    
