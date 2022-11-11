{
    'name':'Website Animate',
    'description':"Provide animation for page\'s blocks",
    'category': 'Website',
    'version':'1.1',
    'author':'Odoo S.A.',
    'data': [
        # 'views/assets.xml',
        'views/options.xml',
    ],
    'depends': ['website'],
    'assets': {
        'web.assets_frontend': [
            '/website_animate/static/src/scss/o_animate_frontend.scss',
            '/website_animate/static/src/js/o_animate.frontend.js',
            '/website_animate/static/src/js/o_animate.editor.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
}
