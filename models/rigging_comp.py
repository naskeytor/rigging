from odoo import models, fields, api

class Comp(models.Model):
    _name = 'rigging.comp'
    _description = 'Component'

    name = fields.Char(string="Serial Number")
    compt_id = fields.Many2one('rigging.compt', string="Component Type")
    compt = fields.Char(related='compt_id.name', string='Type component')

    model_id = fields.Many2one('rigging.model', string="Model_ID")
    model = fields.Char(related="model_id.name", string="Model")
    model_component = fields.Char(compute='_model_component', string="Canopy Model")

    size_id_canopy = fields.Many2one('rigging.canopy.size', string="Size Canopy")
    size_id_container = fields.Many2one('rigging.container.size', string="Size Container")
    size = fields.Char('Size', compute='_compute_size')

    dom = fields.Date()




    @api.depends('size_id_canopy.name', 'size_id_container.name', 'size', 'compt')
    def _compute_size(self):
        for record in self:
            if record.compt == "Reserve" or record.compt == "Canopy":
                record.size = record.size_id_canopy.name
            else:
                record.size = record.size_id_container.name


    rigging_ids = fields.Many2one('rigging.rigging')

    # compute in model-size format
    @api.depends("model", "compt", "size")            # Set up the model for better visibility
    def _model_component(self):
        for record in self:
            if record.compt == "Reserve" or record.compt == "Canopy":
                record.model_component = str(record.model) + "-" + str(record.size)
            else:
                record.model_component = str(record.model)

    # setup date
