from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ComponentModel(models.Model):
    _name = 'rigging.rigs'
    _description = 'Rigs'
    

    name = fields.Char(string='Rig Number')

    comp_ids = fields.Many2one('rigging.comp')

    canopy_id = fields.Many2one('rigging.comp', domain=['&', ('compt', '=', 'Canopy'), ('is_mounted', '=', False)])
    container_id = fields.Many2one('rigging.comp', domain=['&', ('compt', '=', 'Container'), ('is_mounted', '=', False)])
    reserve_id = fields.Many2one('rigging.comp', domain=['&', ('compt', '=', 'Reserve'), ('is_mounted', '=', False)])
    aad_id = fields.Many2one('rigging.comp', domain=['&', ('compt', '=', 'Aad'), ('is_mounted', '=', False)])

    status_id = fields.Many2one( 'rigging.status' )

    rig_canopy_model = fields.Char(related="canopy_id.model_component", string="Canopy Model")
    rig_container_model = fields.Char(related="container_id.model_component", string="Container Model")
    rig_reserve_model = fields.Char(related="reserve_id.model_component", string="Reserve Model")
    rig_aad_model = fields.Char(related="aad_id.model_component", string="AAD Model")

    rig_canopy_full = fields.Char(related="canopy_id.full_component", string="Canopy Info", store=True, readonly=False)

    #state = fields.Char('State', compute='_compute_state_component', store=True)


    #canopy_id = fields.Many2one( 'rigging.canopy', domain=[('is_mounted', '=', False )] )
    """container_id = fields.Many2one( 'rigging.container', domain=[('is_mounted', '=', False )] )
    reserve_id = fields.Many2one( 'rigging.reserve' , domain=[('is_mounted', '=', False )])
    aad_id = fields.Many2one( 'rigging.aad', domain=[('is_mounted', '=', False )] )

    rig_canopy_model = fields.Char(related="canopy_id.model_canopy", string="Canopy Model")
    rig_container_model = fields.Char( related="container_id.model", string="Container Model")
    rig_reserve_model = fields.Char( related="reserve_id.model_reserve", string="Reserve Model")
    rig_aad_model = fields.Char( related="aad_id.model", string="AAD Model")
    
    #mounted_canopy = fields.Char( related="canopy_id.mounted", string="Canopy", store=True)
    rigging_id = fields.Many2one('rigging.rigging')
    reserve_repack = fields.Date('Date Last Revision')
    reserve_next = fields.Date('Date Next Revision', compute='_next_reserve_repack')"""

    umount_component = fields.Selection(
        string = "Component",
        selection =[
            ('container', 'Container'),
            ('canopy', 'Canopy'),
            ('reserve', 'Reserve'),
            ('aad', 'Aad')
        ]
    )

    def action_umount_component(self):
        if self.umount_component == "canopy":
            self.canopy_id.rig_id = False
            self.canopy_id.is_mounted = False
            self.canopy_id = False
            self.umount_component = False
        elif self.umount_component == "container":
            self.container_id.rig_id = False
            self.container_id.is_mounted = False
            self.container_id = False
            self.umount_component = False
        elif self.umount_component == "reserve":
            self.reserve_id.rig_id = False
            self.reserve_id.is_mounted = False
            self.reserve_id = False
            self.umount_component = False
        else:
            self.aad_id.rig_id = False
            self.aad_id.is_mounted = False
            self.aad_id = False
            self.umount_component = False


    """@api.depends('reserve_repack', 'reserve_next')
    def _next_reserve_repack(self):
        for record in self:
            if record.reserve_repack:
                record.reserve_next = record.reserve_repack + relativedelta(years=1)
            else:
                record.reserve_next = False"""

    @api.onchange('canopy_id', 'container_id', 'reserve_id', 'aad_id')
    def _onchange_component(self):
        self.canopy_id.rig_id = self._origin
        self.container_id.rig_id = self._origin
        self.reserve_id.rig_id = self._origin
        self.aad_id.rig_id = self._origin




    rigging_ids = fields.One2many('rigging.rigging', 'rig_id', string="Rigging")




    """def action_umount_canopy_rig(self):
        self.canopy_id.rig_id = False
        self.canopy_id.is_mounted = False
        self.canopy_id = False"""

    def action_mount_canopy_rig(self):
        self.canopy_id.rig_id = self.id

    """@api.onchange('canopy_id')
    def _mount_canopy_rig(self):
        self.canopy_id = self._origin"""

    """@api.depends('comp_ids.is_mounted')  # Set up the mounting status
    def _compute_state_component(self):
        for record in self:
            if record.comp_ids.is_mounted == True:
                record.state = "Mounted"
                record.comp_ids.is_mounted = True
            else:
                record.state = "Unmounted"""""





        
