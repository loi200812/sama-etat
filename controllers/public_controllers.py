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
        project = request.env['government.project'].sudo().browse(project_id).read(['name', 'description', 'project_code', 'status', 'priority', 'ministry_id', 'manager_id', 'start_date', 'end_date', 'progress', 'strategic_objective_id', 'budget_id', 'task_count', 'write_date', 'latitude', 'longitude'])[0]
        if not project:
            return request.render('website.404')
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
        decision = request.env['government.decision'].sudo().browse(decision_id).read(['name', 'title', 'reference', 'decision_type', 'decision_date', 'document', 'document_name', 'description', 'status', 'strategic_objective_id', 'project_id', 'event_id', 'ministry_id', 'is_public', 'implementation_status', 'implementation_deadline', 'responsible_user_id', 'progress_percentage', 'last_follow_up_date', 'next_follow_up_date', 'follow_up_notes', 'is_on_track', 'days_until_deadline', 'latitude', 'longitude'])[0]
        if not decision:
            return request.render('website.404')
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
        event_data = request.env['government.event'].sudo().browse(event_id).read(['name', 'event_date', 'date_start', 'date_end', 'location', 'organizer_id', 'event_type', 'description', 'project_id', 'strategic_objective_id', 'status', 'odoo_event_id', 'latitude', 'longitude'])
        if not event_data:
            return request.render('website.404')
        event = event_data[0]
        if not event:
            return request.render('website.404')
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

    @http.route('/senegal2050/objective/<int:objective_id>', type='http', auth='public', website=True)
    def public_objective_page(self, objective_id, **kw):
        objective = request.env['strategic.objective'].sudo().browse(objective_id).read(['name', 'code', 'axis_id', 'description', 'kpi_ids', 'linked_projects', 'linked_decisions', 'linked_budgets', 'linked_events'])[0]
        if not objective:
            return request.render('website.404')

        # Generate QR code for the objective URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        objective_url = f"{base_url}/senegal2050/objective/{objective_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(objective_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_objective_page', {
            'objective': objective,
            'objective_url': objective_url,
            'qr_code': qr_code_base64,
        })

    @http.route('/senegal2050/axis/<int:axis_id>', type='http', auth='public', website=True)
    def public_axis_page(self, axis_id, **kw):
        axis = request.env['strategic.axis'].sudo().browse(axis_id).read(['name', 'code', 'description', 'pillar_id', 'objective_ids'])[0]
        if not axis:
            return request.render('website.404')

        # Generate QR code for the axis URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        axis_url = f"{base_url}/senegal2050/axis/{axis_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(axis_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_axis_page', {
            'axis': axis,
            'axis_url': axis_url,
            'qr_code': qr_code_base64,
        })

    @http.route('/senegal2050/pillar/<int:pillar_id>', type='http', auth='public', website=True)
    def public_pillar_page(self, pillar_id, **kw):
        pillar = request.env['strategic.pillar'].sudo().browse(pillar_id).read(['name', 'code', 'description', 'plan_id', 'axis_ids'])[0]
        if not pillar:
            return request.render('website.404')

        # Generate QR code for the pillar URL
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        pillar_url = f"{base_url}/senegal2050/pillar/{pillar_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(pillar_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return request.render('sama_etat.public_pillar_page', {
            'pillar': pillar,
            'pillar_url': pillar_url,
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