odoo.define('website_ecommerce_snippets_blocks_ul_73lines.as_img_hotspot', function (require) {
"use strict";

var core = require('web.core');
var options = require('web_editor.snippets.options');
var wUtils = require('website.utils');
var weWidgets = require('wysiwyg.widgets');
var _t = core._t;
var popoverShow = false;

options.SnippetOptionWidget.include({
    events: {
        'click .add_img_hotspot':'_addIcon',
        'click .o_we_collapse_toggler': '_onCollapseTogglerClick',
    },
    _addIcon:function(){
        var $block = '<div class="row hotspot"><p style="position: absolute;top:50%;left: 50%;transform: translate(-50%, -50%);" class="hotspot_icon actv" data-name="Block">\
        <a href="#" class="hotspot-icon-ultimate">hotspot-icon</a>\
        </p></div>';
        this.$target.after($block);
        this.$target.parent().find('.actv').trigger('click').removeClass('actv');
    }
});

options.registry.img_hotspots_slider_actions = options.Class.extend({
    events:{
        'click we-button.add_preview':'_Preview',
        'change we-range.pos_left':'_applyLeft',
        'change we-range.pos_top':'_applyRight',
        'click we-select.hs_types':'_applyType',
        'click we-button.modal_tpy':'_removePS',
        'click we-button.pop_tpy':'_applyPopoverDy',
        'click we-button.add_product':'_applyProduct',
        'click .imagebox':'_applyImage',
        'click .style_icon':'_applyIcon'
    },
    popup_template_id: "Product_select_template",
    popup_title: _t("Add Popover Product"),
    _applyIcon:function(evt){
        var getCls = $(evt.currentTarget).attr('data-select-data-attribute')
        this.$target.removeClass('style1 style2 style3').addClass(getCls)
    },
    _applyImage:function(){
        var self = this;
        var dialog = new weWidgets.MediaDialog(this, {multiImages: false, onlyImages: true, mediaWidth: 1920});
        return new Promise(resolve => {
            dialog.on('save', this, function (attachments) {
                self.$target.attr('data-popup_imgurl',$(attachments).attr('src'))
            });
            dialog.on('closed', this, () => resolve());
            dialog.open();
        });
    },
    _applyProduct:function(){
        var self = this
        var def = wUtils.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Product"),
            'init': function (field) {
                var $field = field;
                var formatState = function(state){
                    if(!state.id){
                        return state.text;
                    }
                    var optimage = $(state.element).attr('data-image');
                    var $state = $(
                        '<span><img src="'+optimage+'" style="width:60px;height:auto;margin-right: 10px;"/>' + state.text + '</span>'
                        );
                    return $state;
                }
                self._rpc({
                    route: '/get/product_all/',
                    params: {}
                }).then(function (result) {
                    for (const prod of result) {
                        var opt = "<option value='"+ prod['id'] +"' data-image='"+prod.image_url+"'>"+ prod['text'] +"</option>"
                        $field.append(opt);
                    }
                });
                $field.select2({
                    width:'100%',
                    formatResult:formatState,
                })
                var getproid = self.$target.attr('data-product_template_id');
                var getname =  self.$target.attr('data-product_name');
                if(getproid != undefined && getname != undefined){
                    $field.select2('data',{'id':getproid,'text':getname})
                }
            },
        });
        def.then(function (data) {
            self.$target.attr('data-product_template_id',data.val);
            self._rpc({
                route: '/get/product_detail/',
                params: {'id':data.val,'name_only':true}
            }).then(function (result) {
                self.$target.attr('data-product_name',result);
            });

        });
        return def
    },
    _applyPopoverDy:function(){
        var popoverhtm = "<div class='media'><h2>No Product Seleted</h2></div>";
        this.$target.children().attr('data-toggle','popover').attr('data-html',true).attr('data-content',popoverhtm);
    },
    _removePS:function () {
        this.$target.removeAttr('data-popup_style');
        this.$target.children().removeAttr('data-toggle data-html data-content');
    },
    _Preview:function(){
        if(popoverShow === false){
            var title = this.$target.attr('data-popup_title') == undefined ? 'Title':this.$target.attr('data-popup_title');
            var description = this.$target.attr('data-popup_desc') == undefined ? 'description':this.$target.attr('data-popup_desc');
            var btn_txt = this.$target.attr('data-popup_btntext') == undefined ? 'text':this.$target.attr('data-popup_btntext');
            var btn_url = this.$target.attr('data-popup_btnurl') == undefined ? '/':this.$target.attr('data-popup_btnurl');
            var img_url = this.$target.attr('data-popup_imgurl') == undefined ? '/website_ecommerce_snippets_blocks_ul_73lines/static/src/img/snippets/image.png' :this.$target.attr('data-popup_imgurl');
            var pop_thm = this.$target.attr('data-popup_theme') == undefined ? '' :this.$target.attr('data-popup_theme');
            var pop_style = this.$target.attr('data-popup_style') == undefined ? '' :this.$target.attr('data-popup_style');
            var style_cls = pop_thm + " " + pop_style;
            var popoverhtm = "<div class='hotspot-media "+ style_cls +"'>\<div class='hotspot-image'><img src='"+img_url+"' alt='Image' class='img-fluid'></div>\<div class='hotspot-body-content'>\<h5 class='hotspot-title'>"+ title +"</h5><p>"+description+"</p><a href='"+btn_url+"' class='as-btn btn-primary btn-sm'>"+ btn_txt +"</a></div></div>";
            this.$target.children().removeAttr('data-original-title').removeAttr('title');
            this.$target.children().attr('data-content',popoverhtm);
            var getData = this.$target.find('[data-toggle="popover"]').popover();
            this.$target.find('[data-toggle="popover"]').popover('show');
            var getid = "#" + $(getData['0']).attr('aria-describedby');
            $(getid).removeClass('theme_dark theme_light style1 style2 style3');
            style_cls =  'popover-hotspot' + '  '+ style_cls;
            $(getid).addClass(style_cls);
            popoverShow = true;
        }
        else{
            this.$target.find('[data-toggle="popover"]').popover('hide');
            popoverShow = false;
        }

    },
    _applyLeft:function(){
        var posval = this.$target.attr('data-pos_left');
        posval = posval+"%";
        this.$target.css('left',posval);
    },
    _applyRight:function(){
        var posval = this.$target.attr('data-pos_top');
        posval = posval+"%";
        this.$target.css('top',posval);
    },
    _applyType:function(){
        if(this.$target.hasClass('static_type')){
            this.$target.children().attr('data-toggle','popover').attr('data-html',true).attr('data-content','')
        }
        else if(this.$target.hasClass('design_dynamic')){
            this.$target.children().removeAttr('data-toggle data-html data-content');
            this.$target.removeAttr('data-popup_title data-popup_desc data-popup_btntext data-popup_imgurl data-popup_btnurl data-popup_style data-popup_theme').attr('data-product_template_id','0')
        }
    },
    cleanForSave:function(){
        if(popoverShow == true){
            this._Preview();
        }
        $(".hotspot_icon").each(function (index, element) {
            if($(this).hasClass("static_type") === false && $(this).hasClass("design_dynamic") == false){
                $(this).parent().remove();;
            }
        });
    }
});
});
