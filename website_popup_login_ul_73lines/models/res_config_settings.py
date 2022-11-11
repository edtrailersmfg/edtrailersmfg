from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_login_ul_73lines_option = fields.Selection([
        ('default', 'Default LogIn'),
        ('website_popup_login_ul_73lines_option', 'Enable LogIn In Pop Up'),
        ('website_sidebar_login_ul_73lines_option', 'Enable LogIn In Sidebar'),
    ], 'Login Types', config_parameter='website_popup_login_ul_73lines.website_login_ul_73lines_option', default='default')