from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ComponentModel(models.Model):
    _name = 'rigging.rigs'
    _description = 'Rigs'
    

    name = fields.Char()
    status_id = fields.Many2one( 'rigging.status' )
    
    canopy_id = fields.Many2one( 'rigging.canopy', domain=[('is_mounted', '=', False )] )
    container_id = fields.Many2one( 'rigging.container', domain=[('is_mounted', '=', False )] )
    reserve_id = fields.Many2one( 'rigging.reserve' , domain=[('is_mounted', '=', False )])
    aad_id = fields.Many2one( 'rigging.aad', domain=[('is_mounted', '=', False )] )

    rig_canopy_model = fields.Char( related="canopy_id.model_canopy", string="Canopy Model" )
    rig_container_model = fields.Char( related="container_id.model", string="Container Model")
    rig_reserve_model = fields.Char( related="reserve_id.model_reserve", string="Reserve Model")
    rig_aad_model = fields.Char( related="aad_id.model", string="AAD Model")
    
    mounted_canopy = fields.Char( related="canopy_id.mounted", string="Canopy", store=True)
    rigging_id = fields.Many2one('rigging.rigging')
    reserve_repack = fields.Date('Date Last Revision')
    reserve_next = fields.Date('Date Next Revision', compute='_next_reserve_repack')

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
            pass
        elif self.umount_component == "reserve":
            pass
        else:
            pass


    @api.depends('reserve_repack', 'reserve_next')
    def _next_reserve_repack(self):
        for record in self:
            if record.reserve_repack:
                record.reserve_next = record.reserve_repack + relativedelta(years=1)
            else:
                record.reserve_next = False

    @api.onchange('canopy_id')
    def _onchange_canopy(self):
        self.canopy_id.rig_id = self._origin
        



    rigging_ids = fields.One2many('rigging.rigging', 'rig_id', string="Rigging")




    def action_umount_canopy_rig(self):
        self.canopy_id.rig_id = False
        self.canopy_id.is_mounted = False
        self.canopy_id = False

    def action_mount_canopy_rig(self):
        self.canopy_id.rig_id = self.id




        
