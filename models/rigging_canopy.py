from odoo import models, fields, api

class Canopy(models.Model):
    _name = 'rigging.canopy'
    _description = 'Canopy'

    sn = fields.Char()
    #model_id = fields.One2many( 'rigging.model', 'component_id'  )

    prueba = fields.Char()
