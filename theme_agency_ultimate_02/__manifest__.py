# -- encoding: utf-8 --
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': "Theme Agency Ultimate 02",
    'description': "Theme Agency Ultimate 02 By 73Lines",
    'category': "Theme",
    'author': "73lines",
    'summury': "Theme Agency Ultimate 02 ",
    'Website': "https://www.73lines.com",
    'version': "13.0.1.0",
    'depends': ["ultimate_website_tools_business",
                "website_business_snippets_blocks_blog_ul_73lines",
                "website_business_snippet_blocks_crm_ul_73lines"],
    'data':[
        "views/assets.xml",
        "views/templates.xml",
        "views/theme_data.xml",
        "views/image_library.xml",
        "views/footer.xml"
    ],
     'images': [
         'static/description/agency_ultimate_02_screenshot.png',
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/theme_agency_ultimate_02/static/src/scss/primary_variables.scss',

        ],
        'web.assets_frontend': [
            '/theme_agency_ultimate_02/static/src/scss/style.scss',

        ],
    },
     'license': "OPL-1",
}