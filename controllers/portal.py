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

        containers = components.filtered(lambda c: c.component_type == 'container')
        reserves = components.filtered(lambda c: c.component_type == 'reserve')

        values = {
            'page_name': 'rigging_dashboard',
            'rigs': rigs,
            'canopies': components.filtered(lambda c: c.component_type == 'canopy'),
            'containers': containers,
            'reserves': reserves,
            'aads': components.filtered(lambda c: c.component_type == 'aad'),
            'rigging_jobs': rigging_jobs,
            'has_tandem_containers': any(c.usage_type == 'tandem' for c in containers),
            'has_tandem_reserves': any(r.usage_type == 'tandem' for r in reserves),
        }
        return request.render('rigging.portal_rigging_dashboard', values)

    @route(['/my/rigging/component/<int:component_id>'], type='http', auth='user', website=True)
    def portal_component_detail(self, component_id, **kw):
        # search respects the portal security rule (owner_id = current partner)
        component = request.env['rigging.component'].search([('id', '=', component_id)])
        if not component:
            return request.not_found()

        rigging_jobs = request.env['rigging.rigging'].search(
            [('component_id', '=', component_id)], order='date desc', limit=20
        )

        return request.render('rigging.portal_component_detail', {
            'page_name': 'rigging_component',
            'component': component,
            'rigging_jobs': rigging_jobs,
        })
