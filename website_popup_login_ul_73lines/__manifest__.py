{
    'name': "Popup LogIn",
    'author': '73Lines',
    'installable': True,
    'summary': 'Log In Popup',
    'category': 'Tools',
    'version': '14.0.1.0.1',
    'website': 'https://www.73lines.com/',
    'images': [],
    'depends': ['base',
                'website',
                'auth_oauth',
                'auth_signup'],

    'data': ['views/res_config_settings_view.xml',
             'views/portal_sign_in.xml',
             'views/assets.xml'],

    'qweb': ['static/src/xml/*.xml'],

    'assets': {
            'web.assets_frontend': [
                '/website_popup_login_ul_73lines/static/src/css/popup_login.scss',
                '/website_popup_login_ul_73lines/static/src/scss/sidebar_login.scss',

                '/website_popup_login_ul_73lines/static/src/js/script.js',
                '/website_popup_login_ul_73lines/static/src/js/login_slidebar.js',
            ],
    },

    'demo': [],
    'license': 'OPL-1',
}

