from odoo import models, fields, api

class Comp(models.Model):
    _name = 'rigging.comp'
    _description = 'Component'

    name = fields.Char(string="Serial Number")
    compt_id = fields.Many2one('rigging.compt', string="Component Type")
    model_id = fields.Many2one('rigging.model', string="Model_ID")
    model = fields.Char(related="model_id.name", string="Model")
    #size_id = fields.Many2one('rigging.canopy.size', string="Size")
    #size = fields.Char(related="size_id.name", string="Size ID")
    size_id_canopy = fields.Many2one('rigging.canopy.size', string="Size Canopy")
    size_id_container = fields.Many2one('rigging.container.size', string="Size Container")
    size = fields.Char('Size', compute='_compute_size')
    #size = fields.Char(related="size_id.name", string="Size ID")

    @api.depends('size_id_canopy.name', 'size_id_container', 'size', 'compt_id')
    def _compute_size(self):
        for record in self:
            if record.compt_id == "Canopy":
                record.size = record.size_id_canopy.name
            else:
                record.size = record.size_id_container.name

    rigging_ids = fields.Many2one('rigging.rigging')
