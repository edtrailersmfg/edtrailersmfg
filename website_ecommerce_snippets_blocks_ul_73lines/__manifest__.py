# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Ecommerce Snippets Blocks',
    'description': 'Ecommerce Snippets Blocks',
    'category': "Ecommerce",
    'author': "73Lines",
    'website': "https://www.73lines.com/",
    'version': "14.0.1.0.1",
    'depends': [

        # Default Modules
        'website',
        'mass_mailing',
        'website_sale_wishlist',
        'website_sale_comparison',

        # Ultimate Website Tools Modules
        'website_business_snippet_blocks_core_ul_73lines',

        # 73lines Modules
        'website_snippet_product_carousel_ul_73lines',
        'website_product_misc_options_ul_73lines',
        'website_product_quick_view_ul_73lines',
        'website_product_categ_menu_and_banner_ul_73lines',
        # 'website_product_ribbon_ul_73lines',
        'website_product_share_options_ul_73lines',
        'website_product_page_layout_ul_73lines',

    ],
    'data': [
        'views/assets.xml',
        'views/product_template.xml',
        'views/collapse_categories.xml',
        'views/res_config_settings.xml',

        # ecommerce block

        'views/snippets/ecommerce_block/ecommerce_block_1.xml',
        'views/snippets/ecommerce_block/ecommerce_block_2.xml',
        'views/snippets/ecommerce_block/ecommerce_block_3.xml',
        'views/snippets/ecommerce_block/ecommerce_block_4.xml',
        'views/snippets/ecommerce_block/ecommerce_block_5.xml',
        'views/snippets/ecommerce_block/ecommerce_block_6.xml',
        'views/snippets/ecommerce_block/ecommerce_block_7.xml',
        'views/snippets/ecommerce_block/ecommerce_block_8.xml',
        'views/snippets/ecommerce_block/ecommerce_block_9.xml',
        'views/snippets/ecommerce_block/ecommerce_block_10.xml',
        'views/snippets/ecommerce_block/ecommerce_block_11.xml',
        'views/snippets/ecommerce_block/ecommerce_block_12.xml',
        'views/snippets/ecommerce_block/ecommerce_block_13.xml',
        'views/snippets/ecommerce_block/ecommerce_block_14.xml',
        'views/snippets/ecommerce_block/ecommerce_block_15.xml',
        'views/snippets/ecommerce_block/ecommerce_block_16.xml',
        'views/snippets/ecommerce_block/ecommerce_block_17.xml',

        #image grid

        'views/snippets/image_grid/image_grid_1.xml',
        'views/snippets/image_grid/image_grid_2.xml',
        'views/snippets/image_grid/image_grid_3.xml',
        'views/snippets/image_grid/image_grid_4.xml',
        'views/snippets/image_grid/image_grid_5.xml',
        'views/snippets/image_grid/image_grid_6.xml',
        'views/snippets/image_grid/image_grid_7.xml',
        'views/snippets/image_grid/image_grid_8.xml',
        'views/snippets/image_grid/image_grid_9.xml',
        'views/snippets/image_grid/image_grid_10.xml',
        'views/snippets/image_grid/image_grid_11.xml',
        'views/snippets/image_grid/image_grid_12.xml',
        'views/snippets/image_grid/image_grid_13.xml',
        'views/snippets/image_grid/image_grid_14.xml',
        'views/snippets/image_grid/image_grid_15.xml',
        'views/snippets/image_grid/image_grid_16.xml',
        'views/snippets/image_grid/image_grid_17.xml',
        'views/snippets/image_grid/image_grid_18.xml',
        'views/snippets/image_grid/image_grid_19.xml',
        'views/snippets/image_grid/image_grid_20.xml',

        #product carousel

        'views/snippets/product_carousel/carousel_design_1.xml',
        'views/snippets/product_carousel/carousel_design_2.xml',
        'views/snippets/product_carousel/carousel_design_3.xml',
        'views/snippets/product_carousel/carousel_design_4.xml',
        'views/snippets/product_carousel/carousel_design_5.xml',
        'views/snippets/product_carousel/carousel_design_6.xml',
        'views/snippets/product_carousel/carousel_design_7.xml',
        'views/snippets/product_carousel/carousel_design_8.xml',
        'views/snippets/product_carousel/carousel_design_9.xml',
        'views/snippets/product_carousel/carousel_design_10.xml',
        'views/snippets/product_carousel/carousel_design_11.xml',
        'views/snippets/product_carousel/carousel_design_12.xml',
        'views/snippets/product_carousel/carousel_design_13.xml',
        'views/snippets/product_carousel/carousel_design_14.xml',
        'views/snippets/product_carousel/carousel_design_15.xml',
        'views/snippets/product_carousel/carousel_design_16.xml',
        'views/snippets/product_carousel/carousel_design_17.xml',
        'views/snippets/product_carousel/carousel_design_18.xml',
        'views/snippets/product_carousel/carousel_design_19.xml',
        'views/snippets/product_carousel/carousel_design_20.xml',
        'views/snippets/product_carousel/carousel_design_21.xml',
        'views/snippets/product_carousel/carousel_design_22.xml',
        'views/snippets/product_carousel/carousel_design_23.xml',
        'views/snippets/product_carousel/carousel_design_24.xml',
        'views/snippets/product_carousel/carousel_design_25.xml',
        'views/snippets/product_carousel/carousel_design_26.xml',
        'views/snippets/product_carousel/carousel_design_27.xml',
        'views/snippets/product_carousel/carousel_design_28.xml',
        'views/snippets/product_carousel/carousel_design_29.xml',
        'views/snippets/product_carousel/carousel_design_30.xml',

        #product mini carousel
        'views/snippets/product_mini_carousel/product_mini_carousel_1.xml',
        'views/snippets/product_mini_carousel/product_mini_carousel_2.xml',
        'views/snippets/product_mini_carousel/product_mini_carousel_3.xml',
        'views/snippets/product_mini_carousel/product_mini_carousel_4.xml',
        'views/snippets/product_mini_carousel/product_mini_carousel_5.xml',

         #product Tab carousel
        'views/snippets/product_tab_carousel/product_tab_carousel_1.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_2.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_3.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_4.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_5.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_6.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_7.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_8.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_9.xml',
        'views/snippets/product_tab_carousel/product_tab_carousel_10.xml',

        #ecommerce mid header

        'views/snippets/mid_header/ecommerce_mid_header_1.xml',
        'views/snippets/mid_header/ecommerce_mid_header_2.xml',
        'views/snippets/mid_header/ecommerce_mid_header_3.xml',
        'views/snippets/mid_header/ecommerce_mid_header_4.xml',
        'views/snippets/mid_header/ecommerce_mid_header_5.xml',
        'views/snippets/mid_header/ecommerce_mid_header_6.xml',
        'views/snippets/mid_header/ecommerce_mid_header_7.xml',
        'views/snippets/mid_header/ecommerce_mid_header_8.xml',
        'views/snippets/mid_header/ecommerce_mid_header_9.xml',
        'views/snippets/mid_header/ecommerce_mid_header_10.xml',
        'views/snippets/mid_header/ecommerce_mid_header_11.xml',
        'views/snippets/mid_header/ecommerce_mid_header_12.xml',
        'views/snippets/mid_header/ecommerce_mid_header_13.xml',
        'views/snippets/mid_header/ecommerce_mid_header_14.xml',
        'views/snippets/mid_header/ecommerce_mid_header_15.xml',
        'views/snippets/mid_header/ecommerce_mid_header_16.xml',
        'views/snippets/mid_header/ecommerce_mid_header_17.xml',
        'views/snippets/mid_header/ecommerce_mid_header_18.xml',
        'views/snippets/mid_header/ecommerce_mid_header_19.xml',
        'views/snippets/mid_header/ecommerce_mid_header_20.xml',
        'views/snippets/mid_header/ecommerce_mid_header_21.xml',
        'views/snippets/mid_header/ecommerce_mid_header_22.xml',
        'views/snippets/mid_header/ecommerce_mid_header_23.xml',
        'views/snippets/mid_header/ecommerce_mid_header_24.xml',
        'views/snippets/mid_header/ecommerce_mid_header_25.xml',
        'views/snippets/mid_header/ecommerce_mid_header_26.xml',

        #mid header Utilities

        'views/snippets/mid_header_utilities/language_button_1.xml',
        'views/snippets/mid_header_utilities/language_button_2.xml',
        'views/snippets/mid_header_utilities/pricelist_button_1.xml',
        'views/snippets/mid_header_utilities/pricelist_button_2.xml',
        'views/snippets/mid_header_utilities/searchbox_1.xml',
        'views/snippets/mid_header_utilities/searchbox_2.xml',
        'views/snippets/mid_header_utilities/searchbox_3.xml',
        'views/snippets/mid_header_utilities/searchbox_4.xml',
        'views/snippets/mid_header_utilities/searchbox_5.xml',
        'views/snippets/mid_header_utilities/searchbox_6.xml',
        'views/snippets/mid_header_utilities/searchbox_with_dropdown.xml',
        'views/snippets/mid_header_utilities/full_screen_search_d1.xml',
        'views/snippets/mid_header_utilities/full_screen_search_d2.xml',


        # Other
        'views/snippets/ecommerce_block/hotspot_img.xml',

    ],
    'images': [
    ],
    'assets': {
            'web.assets_frontend': [
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/product_carousel_mini_1.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/sinlge_product_page.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/product_tab_carousel.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/carousel.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/ecommerce_block.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/image_grid.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/carousel_design.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/mini_carousel.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/mid_header.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/mid_header_utilities.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/custom_carousel.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/css/owl.carousel.css',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/library/photoswipe/photoswipe.css',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/library/photoswipe/default-skin.css',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/img_hotspot/000.scss',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/img_hotspot/hotspot.scss',

                # '/website_ecommerce_snippets_blocks_ul_73lines/static/src/scss/product_multi_image.scss',

                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/search.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/shop_page.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/full_search.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/owl.carousel.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/library/photoswipe/photoswipe.min.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/library/photoswipe/photoswipe-ui-default.min.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/product_imagezoom.js',
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/img_hotspot/000.js',

                # '/website_ecommerce_snippets_blocks_ul_73lines/static/src/js/jquery.mCustomScrollbar.min.js',
            ],

            'website.assets_editor':[
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/img_hotspot/options.js'
            ],
            'web.assets_qweb': [
                '/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/search_suggestion_inherit.xml'
            ],

        },

    'price': 150,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': '',
    'application': True
}
