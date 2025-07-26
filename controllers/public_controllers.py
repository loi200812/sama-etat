from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
import base64
import qrcode

class SamaEtatController(http.Controller):

    @http.route('/senegal2050/dashboard', type='http', auth='public', website=True)
    def public_dashboard(self, **kw):
        dashboard_data = request.env['senegal.plan.dashboard'].sudo().get_dashboard()
        
        # Generate QR code for the dashboard URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        dashboard_url = f"{base_url}/senegal2050/dashboard"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(dashboard_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        recent_projects = request.env['government.project'].sudo().search([], order='create_date desc', limit=12)

        return request.render('sama_etat.modern_public_dashboard_page', {
            'total_projects': dashboard_data.total_projects,
            'active_projects': dashboard_data.active_projects,
            'total_ministries': dashboard_data.total_ministries,
            'upcoming_events': dashboard_data.upcoming_events,
            'completed_projects': dashboard_data.completed_projects,
            'public_decisions': dashboard_data.published_decisions,
            'dashboard_url': dashboard_url,
            'qr_code': qr_code_base64,
            'recent_projects': recent_projects,
        })

    @http.route('/senegal2050/project/<int:project_id>', type='http', auth='public', website=True)
    def public_project_page(self, project_id, **kw):
        project = request.env['government.project'].sudo().browse(project_id)
        if not project.exists():
            return request.render('website.404')

        # Generate QR code for the project URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        project_url = f"{base_url}/senegal2050/project/{project_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(project_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_project_page', {
            'project': project,
            'project_url': project_url,
            'qr_code': qr_code_base64,
        })

    @http.route('/senegal2050/ministry/<int:ministry_id>', type='http', auth='public', website=True)
    def public_ministry_page(self, ministry_id, **kw):
        ministry = request.env['government.ministry'].sudo().browse(ministry_id)
        if not ministry.exists():
            return request.render('website.404')

        # Generate QR code for the ministry URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        ministry_url = f"{base_url}/senegal2050/ministry/{ministry_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(ministry_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_ministry_page', {
            'ministry': ministry,
            'ministry_url': ministry_url,
            'qr_code': qr_code_base64,
            'projects': ministry.project_ids.filtered(lambda p: p.status != 'draft'), # Only show non-draft projects
        })

    @http.route('/senegal2050/decision/<int:decision_id>', type='http', auth='public', website=True)
    def public_decision_page(self, decision_id, **kw):
        decision = request.env['government.decision'].sudo().browse(decision_id)
        if not decision.exists():
            return request.render('website.404')

        # Generate QR code for the decision URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        decision_url = f"{base_url}/senegal2050/decision/{decision_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(decision_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_decision_page', {
            'decision': decision,
            'decision_url': decision_url,
            'qr_code': qr_code_base64,
        })

    @http.route('/senegal2050/event/<int:event_id>', type='http', auth='public', website=True)
    def public_event_page(self, event_id, **kw):
        event = request.env['government.event'].sudo().browse(event_id)
        if not event.exists():
            return request.render('website.404')

        # Generate QR code for the event URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        event_url = f"{base_url}/senegal2050/event/{event_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(event_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_event_page', {
            'event': event,
            'event_url': event_url,
            'qr_code': qr_code_base64,
        })

    @http.route('/sama_etat/get_map_data', type='json', auth='public', website=True)
    def get_map_data(self):
        Project = request.env['government.project'].sudo()
        Decision = request.env['government.decision'].sudo()
        Event = request.env['government.event'].sudo()

        projects = Project.search_read([('latitude', '!=', False), ('longitude', '!=', False)],
                                       ['name', 'description', 'latitude', 'longitude'])
        decisions = Decision.search_read([('latitude', '!=', False), ('longitude', '!=', False)],
                                         ['name', 'description', 'latitude', 'longitude'])
        events = Event.search_read([('latitude', '!=', False), ('longitude', '!=', False)],
                                     ['name', 'description', 'latitude', 'longitude'])

        return {
            'projects': projects,
            'decisions': decisions,
            'events': events,
        }