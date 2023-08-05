from odoo import models, fields, api


class InputWizzard(models.TransientModel):
    _name = "rigging.input"
    _description = "Transient model for aad jumps input"

    aad_jumps_input = fields.Integer(string="Aad Jumps Input")

    def save_value(self):
        valor = self.aad_jumps_input

        obj = self.env['rigging.rigs']
        obj.create({'jumps_number_rig': valor})


