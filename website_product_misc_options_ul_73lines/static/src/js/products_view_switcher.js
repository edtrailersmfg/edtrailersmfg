/*
    Part of Odoo Module Developed by 73lines
    See LICENSE file for full copyright and licensing details.
*/
odoo.define('website_product_misc_options_ul_73lines.products_view_switcher', function (require) {
    "use strict";

    $(function(){
        $('.grid_view').attr('disabled', 'disabled');
        var previous_view_mode = localStorage['active_view'];
        if (previous_view_mode == 'grid_view') {
            $('div#grid_list').removeClass("oe_list").addClass('oe_grid oe-height-4');
            $('.grid_view').attr('disabled', 'disabled');
            $('.list_view').removeAttr('disabled');
        }
        if (previous_view_mode == 'list_view') {
            $('div#grid_list').removeClass("oe_grid oe-height-4").addClass('oe_list');
            $('.list_view').attr('disabled', 'disabled');
            $('.grid_view').removeAttr('disabled');
        }

        $('.grid_view').click(function(type){
            if(type['type'] !== "click") return;
            $('div#grid_list').removeClass("oe_list").addClass('oe_grid oe-height-4');
            $('.grid_view').attr('disabled', 'disabled');
            $('.list_view').removeAttr('disabled');
            localStorage['active_view'] = 'grid_view';
        });
        $('.list_view').click(function(type){
            if(type['type'] !== "click") return;
            $('div#grid_list').removeClass("oe_grid oe-height-4").addClass('oe_list');
            $('.list_view').attr('disabled', 'disabled');
            $('.grid_view').removeAttr('disabled');
            localStorage['active_view'] = 'list_view';
        });
    });
});
