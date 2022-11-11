# -- encoding: utf-8 --
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': "Theme Product Ecommerce Ultimate 01",
    'description': "Theme Product Ecommerce Ultimate 01 By 73Lines",
    'category': "Theme",
    'author': "73lines",
    'summury': "Theme Product Ecommerce Ultimate 01 ",
    'Website': "https://www.73lines.com",
    'version': "14.0.1.0",
    'depends': ["theme_product_ultimate_01",
                "ultimate_website_tools_ecommerce",
                "website_business_snippets_blocks_blog_ul_73lines",
                "website_business_snippet_blocks_crm_ul_73lines"],
    'data':[
        "views/assets.xml",
        "views/templates.xml",
        "views/theme_data.xml",
        "views/image_library.xml",
    ],
     'images': [
         'static/description/product_ecommerce_ultimate_01_screenshot.png',
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/theme_product_ecommerce_ultimate_01/static/src/scss/primary_variables.scss',

        ],
    },
     'license': "OPL-1",
}