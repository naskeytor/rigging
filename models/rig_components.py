from odoo import models, fields, api

class RigComponents(models.Model):
    _name = 'rigging.components'
    _description = 'Rig Components'

    name = fields.Char()
    model_id = fields.Many2one('rigging.model', string="Model ID")
    model = fields.Char(related="model_id.name", string="Model")
    model_aad = fields.Char(compute='_model_aad', string="AAD Model")
    status_id = fields.Many2one('rigging.status')
    dom = fields.Date()
    next_rev = fields.Char(compute='_next_rev_date')
    expire = fields.Date()
    rigging_ids = fields.One2many('rigging.rigging', 'aad_id', string="Rigging")
    rig_id = fields.One2many('rigging.rigs', 'aad_id')
    mounted = fields.Char('Mounted ON', compute='_compute_mount')
    is_mounted = fields.Boolean('Mounted', default=False)
    
