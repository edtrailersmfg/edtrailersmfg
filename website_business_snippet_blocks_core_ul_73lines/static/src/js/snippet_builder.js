odoo.define('website_business_snippet_blocks_core_ul_73lines.snippet_builder_js', function(require) {
    "use strict";
//    var ajax = require('web.ajax');
$(document).ready(function(){

     $("div#edit-page-menu").on('click',function(){
        waitForElementToDisplay("div#ultimate_snippet_blocks",1000);
    });
    function waitForElementToDisplay(selector, time) {
        if(document.querySelector(selector)!=null) {
            $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
            /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
            $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
            /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
            $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
            $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
            /*This Is For Ecommerce Snippets Product Brans*/
            $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
            /*This Is For Ecommerce Snippet Product Category*/
            $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");
            $('select#selSnippetCat').select2();




            $("select#selSnippetCat").on('change',function(){
                if($("select#selSnippetCat").val()=='mid_headears')
                {
                    $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");


                }
                else if($("select#selSnippetCat").val()=='grid_structure')
                {
                    $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");


                }
                else if($("select#selSnippetCat").val()=='mega_menu')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='banners')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='grids')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='center_content')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='left_content')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='right_content')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='aboutus')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='tabs')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='accordions')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='process_steps')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='features')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='counters')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='image_blocks')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='portfolios')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='team')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='testimonials')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='progressbar')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }

                else if($("select#selSnippetCat").val()=='price_menu')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }

                else if($("select#selSnippetCat").val()=='pricing')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='news')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='cta')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='timer')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='blockquote')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='flipbox')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='newsletter')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='thumbnail_gallery')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='image_slider')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='social_share_icons')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='footer')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().removeClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='contactus')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().removeClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='ecommerce_blocks')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='image_grid')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='product_carousel')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='product_carousel_mini')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().removeClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='product_tab_carousel')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().removeClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='product_brands_carousel')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().removeClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().addClass("o_hidden");



                }
                else if($("select#selSnippetCat").val()=='product_category_carousel')
                {
                   $("#ultimate_snippet_blocks [data-visible=mid_headears]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grid_structure]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=mega_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=banners]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=grids]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=center_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=left_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=right_content]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=aboutus]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=tabs]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=accordions]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=process_steps]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=features]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=counters]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_blocks]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=portfolios]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=team]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=testimonials]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=progressbar]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=price_menu]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=pricing]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=news]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=cta]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=timer]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=blockquote]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=flipbox]").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=newsletter").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=thumbnail_gallery").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_slider").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=social_share_icons").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=footer").parent().addClass("o_hidden");
                    /*This Is For Business Snippet Blocks Crm(Contact Us Snippets)*/
                    $("#ultimate_snippet_blocks [data-visible=contactus").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Blocks(Ecommerce)*/
                    $("#ultimate_snippet_blocks [data-visible=ecommerce_blocks").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=image_grid").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_carousel_mini").parent().addClass("o_hidden");
                    $("#ultimate_snippet_blocks [data-visible=product_tab_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippets Product Brans*/
                    $("#ultimate_snippet_blocks [data-visible=product_brands_carousel").parent().addClass("o_hidden");
                    /*This Is For Ecommerce Snippet Product Category*/
                    $("#ultimate_snippet_blocks [data-visible=product_category_carousel").parent().removeClass("o_hidden");



                }


            });
            return;
        }
        else {
            setTimeout(function() {
                waitForElementToDisplay(selector, time);
            }, time);
        }
    }
});
});