from odoo import models, fields, api

    
class Aad(models.Model):
    _name = 'rigging.aad'
    _description = 'AAD'

    sn = fields.Char()


class Canopy(models.Model):
    _name = 'rigging.canopy'
    _description = 'Canopy'

    sn = fields.Char()
    #model_id = fields.One2many( 'rigging.model', 'component_id'  )

    prueba = fields.Char()

class Container(models.Model):
    _name = 'rigging.container'
    _description = 'Container'

    sn = fields.Char()

class Reserve(models.Model):
    _name = 'rigging.reserve'
    _description = 'Reserve'

    sn = fields.Char()

