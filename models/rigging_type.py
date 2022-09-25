from odoo import models, fields, api

class Type(models.Model):
    _name = 'rigging.type'
    _description = 'Type'

    name = fields.Char()
