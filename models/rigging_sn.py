
from odoo import models, fields, api

class Type(models.Model):
    _name = 'rigging.serial'
    _description = 'Serial Numbers'

    name = fields.Char()