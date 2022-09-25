from odoo import models, fields, api

class RigComponents(models.Model):
    _name = 'rigging.components'
    _description = 'Rig Components'

    name = fields.Char()
    
