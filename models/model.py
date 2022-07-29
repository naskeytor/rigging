from odoo import models, fields, api

class model(models, Model):
    _name = 'rigging.model'
    _description = 'Model'

    name = fields.Char()
    manifacturer_id = fields.Many2one('rigging.manifacturer', 'rigging.manifacturer.id')
