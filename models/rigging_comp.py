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
    full_component = fields.Char(compute='_model_component', string="Canopy Info", store=True)

    size_id_canopy = fields.Many2one('rigging.canopy.size', string="Size Canopy")
    size_id_container = fields.Many2one('rigging.container.size', string="Size Container")
    size = fields.Char('Size', compute='_compute_size')

    rig_id = fields.Many2one('rigging.rigs')
    location = fields.Char(related='rig_id.name', string='Location', store=True)

    mounted = fields.Char('Location', compute='_compute_mount')
    is_mounted = fields.Boolean('Mounted', default=False)

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
    @api.depends("model", "compt", "size", "name")            # Set up the model for better visibility
    def _model_component(self):
        for record in self:
            if record.compt == "Reserve" or record.compt == "Canopy":
                record.model_component = str(record.model) + "-" + str(record.size)
                record.full_component = str(record.model) + "-" + str(record.size) + " " + "Sn: " + str(record.name)
            else:
                record.model_component = str(record.model)
                record.full_component = str(record.model) + " " + "#" + str(record.name)

    """@api.depends("model", "compt", "size")  # Set up the model for better visibility
    def _model_component(self):
        for record in self:
            if record.compt == "Reserve" or record.compt == "Canopy":
                record.model_component = str(record.model) + "-" + str(record.size)
            else:
                record.model_component = str(record.model)"""

    # set up mounted
    @api.depends('rig_id.name')  # Set up the mounting status
    def _compute_mount(self):
        for record in self:
            record.mounted = record.rig_id.name
            if record.mounted:
                record.is_mounted = True

    @api.onchange('rig_id')
    def _mount_canopy(self):
        if self.compt == "Canopy":
            self.rig_id.canopy_id = self._origin
            self.is_mounted = True
        elif self.compt == "Container":
            self.rig_id.container_id = self._origin
            self.is_mounted = True
        elif self.compt == "Reserve":
            self.rig_id.reserve_id = self._origin
            self.is_mounted = True
        else:
            self.rig_id.aad_id = self._origin
            self.is_mounted = True

    def action_umount(self):
        self.rig_id = False
        self.is_mounted = False


    #lf.rig_id.canopy_id = self._origin
    #self.is_mounted = True


