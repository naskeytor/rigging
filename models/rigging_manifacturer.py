from odoo import models, fields, api

class manifacturer(models.Model):
    _name = 'rigging.manifacturer'
    _description = 'Rigging'


    name = fields.Char()
    #model_id = fields.One2many('rigging.model', 'manifacturer_id')

