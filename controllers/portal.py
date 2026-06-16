from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class RiggingCustomerPortal(CustomerPortal):

    @route(['/my/rigging'], type='http', auth='user', website=True)
    def portal_rigging_dashboard(self, **kw):
        partner = request.env.user.partner_id

        rigs = request.env['rigging.rig'].search([('owner_id', '=', partner.id)])
        components = request.env['rigging.component'].search([('owner_id', '=', partner.id)])
        rigging_jobs = request.env['rigging.rigging'].search(
            [('owner_id', '=', partner.id)], order='date desc'
        )

        values = {
            'page_name': 'rigging_dashboard',
            'rigs': rigs,
            'canopies': components.filtered(lambda c: c.component_type == 'canopy'),
            'containers': components.filtered(lambda c: c.component_type == 'container'),
            'reserves': components.filtered(lambda c: c.component_type == 'reserve'),
            'aads': components.filtered(lambda c: c.component_type == 'aad'),
            'rigging_jobs': rigging_jobs,
        }
        return request.render('rigging.portal_rigging_dashboard', values)
