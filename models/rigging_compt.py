from odoo import models, fields, api

class CompT(models.Model):
    _name = 'rigging.compt'
    _description = 'Component'

    name = fields.Char()