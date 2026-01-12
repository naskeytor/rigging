from odoo import models, fields


class RiggingUserHome(models.TransientModel):
    _name = "rigging.user.home"
    _description = "Rigging User Home"
    name = fields.Char(default="My Equipment")

    def action_open_my_rigs(self):
        partner_id = self.env.user.partner_id.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Rigs',
            'res_model': 'rigging.rig',
            'view_mode': 'list,form',
            'domain': [('owner_id', '=', partner_id)],
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
            }
        }
