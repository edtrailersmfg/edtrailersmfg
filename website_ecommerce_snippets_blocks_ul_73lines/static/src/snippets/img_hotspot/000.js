odoo.define('website_ecommerce_snippets_blocks_ul_73lines.s_img_hotspots', function (require) {
"use strict";

var publicWidget = require('web.public.widget');

publicWidget.registry.img_hotspot = publicWidget.Widget.extend({
    selector:'#wrapwrap',
    disabledInEditableMode: false,
    events:{
        'click a.hotspot-icon-ultimate':'_addHotspot'
    },
    _addHotspot:function(ev){
        if (!this.editableMode){
            var getUsers = $(ev.currentTarget).attr('data-content');
            if(getUsers != undefined){
                var getclass = $(getUsers).attr('class').split(' ');
                getclass.shift();
                getclass = getclass.join(" ");
                var Template = '<div class="popover popover-hotspot '+ getclass + '" style="position: absolute; transform: translate3d(675px, 153px, 0px); top: 0px; left: 0px; will-change: transform;">\
                    <div class="arrow" style="top: 43px;"></div>\
                    <h3 class="popover-header"></h3>\
                    <div class="popover-body">\
                    </div>\
                    </div>';
                $(ev.currentTarget).popover({
                        container: '#wrap',
                        template:Template
                });
                if($(ev.currentTarget).attr('aria-describedby') == undefined){
                    $(ev.currentTarget).trigger('click');
                    console.log("FDffffffffffffffff",$(ev.currentTarget));
                };

            }
        }

    },
    start: function (editable_mode) {
        var self = this;
        if (!self.editableMode){
            var DyanmicDesign = self.$target.find('p.design_dynamic');
            $.each(DyanmicDesign, function (index, eachDOM) {
                var gettype = $(eachDOM).attr('data-dynamic_type');
                var prod_id  = $(eachDOM).attr('data-product_template_id');
                if(gettype == "popover"){
                    var popup_style = $(eachDOM).attr('data-popup_style');
//                    $(eachDOM).children().removeClass("o_quick_view").removeAttr('data-product_template_id',prod_id);
                    self._rpc({
                        route: '/get/product_detail/',
                        params: {'id':prod_id,
                                 'popstyle':popup_style,
                                 'popover':true
                                }
                    }).then(function (result) {
                        $(eachDOM).children().attr('data-toggle','popover').attr('data-html',true).attr('data-content',result);
                    });
                }
                else{
                    $(eachDOM).children().removeAttr('data-toggle').removeAttr('data-html').removeAttr('data-content')
//                    .attr('data-product_template_id',prod_id);
//                    $(eachDOM).children().addClass("o_quick_view");
                }
            });
            var getStaticHs = self.$target.find('p.static_type');
            $.each(getStaticHs, function (index, eachDOM) {
                var title = $(eachDOM).attr('data-popup_title') == undefined ? 'Title':$(eachDOM).attr('data-popup_title');
                var description = $(eachDOM).attr('data-popup_desc') == undefined ? 'description':$(eachDOM).attr('data-popup_desc');
                var btn_txt = $(eachDOM).attr('data-popup_btntext') == undefined ? 'text':$(eachDOM).attr('data-popup_btntext');
                var btn_url = $(eachDOM).attr('data-popup_btnurl') == undefined ? '/':$(eachDOM).attr('data-popup_btnurl');
                var img_url = $(eachDOM).attr('data-popup_imgurl') == undefined ? '/website_ecommerce_snippets_blocks_ul_73lines/static/src/img/snippets/image.png' :$(eachDOM).attr('data-popup_imgurl');
                var pop_thm = $(eachDOM).attr('data-popup_theme') == undefined ? '' :$(eachDOM).attr('data-popup_theme');
                var pop_style = $(eachDOM).attr('data-popup_style') == undefined ? '' :$(eachDOM).attr('data-popup_style');
                var style_cls = pop_thm + " " + pop_style;
                var popoverhtm = "<div class='hotspot-media "+ style_cls +"'>\<div class='hotspot-image'><img src='"+img_url+"' alt='Image' class='img-fluid'></div>\<div class='hotspot-body-content'>\<h5 class='hotspot-title'>"+ title +"</h5><p>"+description+"</p><a href='"+btn_url+"' class='as-btn btn-primary btn-sm'>"+ btn_txt +"</a></div></div>";
                $(eachDOM).children().attr('data-content',popoverhtm);
            });
        }
        else{
            var DyanmicDesign = self.$target.find('p.design_dynamic');
//            $.each(DyanmicDesign, function (index, eachDOM) {
//                $(eachDOM).children().removeClass("o_quick_view");
//            });
        }
    }
});
});
