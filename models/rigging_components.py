from odoo import models, fields, api

    
class Aad(models.Model):
    _name = 'rigging.aad'
    _description = 'AAD'

    name = fields.Char()
    model_id = fields.Many2one( 'rigging.model', string="Model ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    status_id = fields.Many2one( 'rigging.status' )
    dom = fields.Date()
    next_rev = fields.Date()
    expire = fields.Date()

class Canopy(models.Model):
    _name = 'rigging.canopy'
    _description = 'Canopy'

    name = fields.Char(string="Serial number")
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.canopy.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_canopy = fields.Char(compute='_model_canopy', string="Canopy Model")
    dom = fields.Date()
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )

    @api.depends("model", "size")
    def _model_canopy(self):
        for record in self:
            record.model_canopy = str(record.model) + "-" + str(record.size)

class Container(models.Model):
    _name = 'rigging.container'
    _description = 'Container'

    name = fields.Char()
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.container.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_container = fields.Char(compute='_model_container', string="Container Model")
    dom = fields.Date()
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )

    @api.depends("model", "size")
    def _model_container(self):
        for record in self:
            record.model_container = str(record.model) + "-" + str(record.size)

class Reserve(models.Model):
    _name = 'rigging.reserve'
    _description = 'Reserve'


    name = fields.Char(string="Serial number")
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.canopy.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_reserve = fields.Char(compute='_model_reserve', string="Reserve Model")
    dom = fields.Date()
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )

    @api.depends("model", "size")
    def _model_reserve(self):
        for record in self:
            record.model_reserve = str(record.model) + "-" + str(record.size)

