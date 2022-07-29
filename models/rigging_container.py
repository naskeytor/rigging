from odoo import models, fields, api

class Container(models.Model):
    _name = 'rigging.container'
    _description = 'Container'

    sn = fields.Char()
