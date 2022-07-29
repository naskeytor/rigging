from odoo import models, fields, api

class Aad(models.Model):
    _name = 'rigging.aad'
    _description = 'AAD'

    sn = fields.Char()
