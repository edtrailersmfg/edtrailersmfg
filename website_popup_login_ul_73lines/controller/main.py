import odoo
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.service import db, security
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class LogInPopUp(http.Controller):

    @http.route('/web/login_popup', type='json', auth="none", sitemap=False)
    def web_login(self, **kw):
        old_uid = request.uid
        values = request.params.copy()
        try:
            uid = request.session.authenticate(request.session.db, kw.get('login'), kw.get('password'))
            values['error'] = _("success")
            return values
        except odoo.exceptions.AccessDenied as e:
            request.uid = old_uid
            if e.args == odoo.exceptions.AccessDenied().args:
                values['error'] = _("Wrong login/password")
            else:
                values['error'] = e.args[0]

        return values

    @http.route('/web/become_login_popup', type='json', auth="none", sitemap=False)
    def super_user_login_popup(self, **kw):
        old_uid = request.uid
        values = request.params.copy()
        try:
            uid = request.session.authenticate(request.session.db, kw.get('login'), kw.get('password'))
            if request.env.user._is_system():
                uid = request.session.uid = odoo.SUPERUSER_ID
                request.env['res.users']._invalidate_session_cache()
                request.session.session_token = security.compute_session_token(request.session, request.env)
                values['error'] = _("success")
                return values

        except odoo.exceptions.AccessDenied as e:
            request.uid = old_uid
            if e.args == odoo.exceptions.AccessDenied().args:
                values['error'] = _("Wrong login/password")
            else:
                values['coerrorde'] = e.args[0]

        return values

    @http.route('/get/popup_bool_value', type='json', auth="none")
    def get_popup_boolean_value_for_login(self):
        get_param = request.env['ir.config_parameter'].sudo().get_param
        return {
            'website_popup_login_ul_73lines_bool_val': get_param('website_popup_login_ul_73lines.website_login_ul_73lines_option'),
        }


class AuthProviders(OAuthLogin):

    @http.route('/get/providers_popup', type='json', auth="none")
    def get_providers_value_popup(self):
        providers = self.list_providers()
        return providers


class AuthSignupHomePopUp(AuthSignupHome):

    @http.route('/get/reset_password_popup', type='json', auth='none')
    def get_reset_password_value(self):
        pass_val = self.get_auth_signup_config()
        return pass_val
