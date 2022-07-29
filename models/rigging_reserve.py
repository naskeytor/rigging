from odoo import models, fields, api

class Reserve(models.Model):
    _name = 'rigging.reserve'
    _description = 'Reserve'

    sn = fields.Char()
