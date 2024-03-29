from email.policy import default
from xml import dom
from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

    

class Aad(models.Model):
    _name = 'rigging.aad'
    _description = 'AAD'

    name = fields.Char()
    model_id = fields.Many2one( 'rigging.model', string="Model ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    model_aad = fields.Char(compute='_model_aad', string="AAD Model")
    status_id = fields.Many2one( 'rigging.status' )
    dom = fields.Date()
    next_rev = fields.Char(compute='_next_rev_date')
    expire = fields.Date()
    rigging_ids = fields.One2many( 'rigging.rigging', 'aad_id', string="Rigging" )
    rig_id = fields.One2many( 'rigging.rigs', 'aad_id' )
    mounted = fields.Char( 'Mounted ON', compute='_compute_mount' )
    is_mounted = fields.Boolean( 'Mounted', default=False )

    @api.depends('model', 'dom')
    def _next_rev_date(self):
        for record in self:
            if record.model != 'Cypres Cmode':
                record.next_rev = datetime.strftime((record.dom + relativedelta(year=4)), '%m/$y')
            else:
                record.next_rev = record.dom + relativedelta(year=15)

    @api.depends('rig_id.name', 'is_mounted')    # Setup the mounting status
    def _compute_mount(self):
        for record in self:
            record.mounted = record.rig_id.name
            if record.mounted:
                record.is_mounted = True
            else:
                record.is_mounted = False

    def action_umount_aad(self):
        self.is_mounted = False
        self.rig_id = None

    """@api.depends("model", "size")            # Setup the model for better visibility
    def _model_aad(self):
        for record in self:
            record.model_canopy = str(record.model) + "-" + str(record.size)"""


class Canopy(models.Model):
    _name = 'rigging.canopy'
    _description = 'Canopy'

    name = fields.Char(string="Name")
    serial_id = fields.Many2one( 'rigging.serial', string='Serial_ID' )
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.canopy.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_canopy = fields.Char(compute='_model_canopy', string="Canopy Model")
    dom = fields.Date()
    rigging_ids = fields.One2many('rigging.rigging', 'canopy_id', string="Rigging")
    rigging_component = fields.Many2one('rigging.components', string="Component ID")
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )
    rigging_id = fields.Many2one( 'rigging.rigging' )
    rig_id = fields.Many2one( 'rigging.rigs', domain=[('canopy_id', '=', False )] )

    location = fields.Char(related='rig_id.name', string='Location')

    mounted = fields.Char( 'Location', compute='_compute_mount' )
    is_mounted = fields.Boolean( 'Mounted', default=False )

    #comp_id = fields.Many2one( 'rigging.comp', string='Comp_id' )
    #comp = fields.Char( related='comp_id.name', string='Comp' )

    

    ####         Compute methods canopy         ###

    @api.onchange('rig_id')
    def _mount_canopy(self):
        self.rig_id.canopy_id = self._origin
        self.is_mounted = True


    @api.depends('rig_id.name')    # Setup the mounting status
    def _compute_mount(self):
        for record in self:
            record.mounted = record.rig_id.name
            if record.mounted:
                record.is_mounted = True
        

    def action_umount_canopy(self):

        self.is_mounted = False
        self.rig_id.canopy_id = False
        self.rig_id = False

    def mount_canopy(self):
        self.rig_id.canopy_id = self.id
        self.is_mounted = True
         


    @api.depends("model", "size")            # Setup the model for better visibility
    def _model_canopy(self):
        for record in self:
            record.model_canopy = str(record.model) + "-" + str(record.size)

class Container(models.Model):
    _name = 'rigging.container'
    _description = 'Container'

    name = fields.Char()
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.container.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_container = fields.Char(compute='_model_container', string="Container Model")
    dom = fields.Date()
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )
    rigging_id = fields.Many2one( 'rigging.rigging' )
    rig_id = fields.One2many( 'rigging.rigs', 'container_id' )
    mounted = fields.Char( 'Mounted', compute='_compute_mount' )
    is_mounted = fields.Boolean( 'Mounted', default=False )
    
    @api.depends('rig_id.name')
    def _compute_mount(self):
        for record in self:
            record.mounted = record.rig_id.name
            if record.mounted:
                record.is_mounted = True
            else:
                record.is_mounted = False

    def action_umount_container(self):
        self.is_mounted = False
        self.rig_id = None

    @api.depends("model", "size")
    def _model_container(self):
        for record in self:
            record.model_container = str(record.model) + "-" + str(record.size)

class Reserve(models.Model):
    _name = 'rigging.reserve'
    _description = 'Reserve'


    name = fields.Char(string="Serial number")
    model_id = fields.Many2one( 'rigging.model', string="Model_ID" )
    model = fields.Char( related="model_id.name", string="Model" )
    size_id = fields.Many2one( 'rigging.canopy.size', string="Size" )
    size = fields.Char( related="size_id.name", string="Size ID" )
    model_reserve = fields.Char(compute='_model_reserve', string="Reserve Model")
    dom = fields.Date()
    type_id = fields.Many2one( 'rigging.type' )
    status_id = fields.Many2one( 'rigging.status' )
    rigging_id = fields.Many2one( 'rigging.rigging' )
    rig_id = fields.One2many( 'rigging.rigs', 'reserve_id' )
    #mounted = fields.Char( 'Mounted', compute='_compute_mount' )
    mounted = fields.Char( related='rig_id.name', string='Location' )
    is_mounted = fields.Boolean( 'Mounted', default=False )

    
    @api.depends('rig_id.name')
    def _compute_mount(self):
        for record in self:
            record.mounted = record.rig_id.name
            if record.mounted:
                record.is_mounted = True
            else:
                record.is_mounted = False

    def action_umount_reserve(self):
        self.is_mounted = False
        self.rig_id = None

    @api.depends("model", "size")
    def _model_reserve(self):
        for record in self:
            record.model_reserve = str(record.model) + "-" + str(record.size)



class SerialNumbers(models.Model):
    _name = 'rigging.serial'
    _description = 'Serial Numbers'


    name = fields.Char(string="Serial number")




