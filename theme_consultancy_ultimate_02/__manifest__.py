# -- encoding: utf-8 --
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': "Theme Consultancy Ultimate 02",
    'description': "Theme Consultancy Ultimate 02 By 73Lines",
    'category': "Theme",
    'author': "73lines",
    'summury': "Theme Consultancy Ultimate 02 ",
    'Website': "https://www.73lines.com",
    'version': "15.0.1.0",
    'depends': ["ultimate_website_tools_business",
                "website_business_snippets_blocks_blog_ul_73lines",
                "website_business_snippet_blocks_crm_ul_73lines"],
    'data':[
        "views/assets.xml",
       # "views/customize_modal.xml",
        "views/templates.xml",
        "views/theme_data.xml",
        "views/image_library.xml",
        "views/footer.xml"
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/theme_consultancy_ultimate_02/static/src/scss/primary_variables.scss',

        ],
    },
     'images': [
         'static/description/consultancy_ultimate_02_screenshot.png',
    ],
     'license': "OPL-1",
}