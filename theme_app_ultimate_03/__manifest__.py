# -- encoding: utf-8 --
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': "Theme App Ultimate 03",
    'description': "Theme App Ultimate 03 By 73Lines",
    'category': "Theme",
    'author': "73lines",
    'summury': "Theme App Ultimate 03 ",
    'Website': "https://www.73lines.com",
    'version': "14.0.1.0",
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
         'static/description/app_ultimate_03_screenshot.png',
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/theme_app_ultimate_03/static/src/scss/primary_variables.scss',

        ],
    },
     'license': "OPL-1",
}