odoo.define('website_popup_login_ul_73lines.script', function (require) {
    "use strict";
    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
    var wUtils = require('website.utils');
    publicWidget.registry.PopUpLogInWidget = publicWidget.Widget.extend({
        selector: '#top_menu_collapse',
        events:{
        'click .popup_super_user': '_OnSuperUserButton',
        'click .login_popup': '_OnLogIn'
        },
        xmlDependencies:['/website_popup_login_ul_73lines/static/src/xml/sign_in_template.xml'],
        init: function(){
            this._super.apply(this,arguments);
        },
        start: function () {
            var self = this;
            ajax.jsonRpc('/get/popup_bool_value', 'call', {
            }).then(function(result){
                if(result['website_popup_login_ul_73lines_bool_val'] == 'website_popup_login_ul_73lines_option'){
                    self.$el.find('.sign_in_without_popup').attr('data-toggle','modal');
                    self.$el.find('.sign_in_without_popup').attr('data-target','#website_popup_login_ul_73lines_modal');

                }else{
                    self.$el.find('.sign_in_without_popup').attr('href','/web/login');
                }
                if(result['website_popup_login_ul_73lines_bool_val'] == 'website_sidebar_login_ul_73lines_option'){
                    self.$el.find('.my_login_sidebar').removeClass('d-none');
                    self.$el.find('.sign_in_without_popup').addClass('d-none');
                    self.$el.find('.categories-filter-drawer-login').removeClass('d-none');

                }else{
                    self.$el.find('.my_login_sidebar').attr('href','/web/login');
                }
            });
            ajax.jsonRpc('/get/providers_popup', 'call', {
            }).then(function(result){
                if(result){
                    self.$el.find('.provider_render_class').html(qweb.render('providers_template',{
                    'providers': result
                    }));
                }
            });
            ajax.jsonRpc('/get/reset_password_popup', 'call', {
            }).then(function(result){
                if(result){
                    self.$el.find('.reset_password_render_class').html(qweb.render('reset_password_popup_template',{
                    'reset_password_enabled': result['reset_password_enabled'],
                    'signup_enabled': result['signup_enabled']
                    }));
                }
            });
        },
        _OnLogIn:function(e){
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var login = this.$el.find('#login').val();
            var password = this.$el.find('#password').val();
            ajax.jsonRpc('/web/login_popup', 'call', {'login': login, 'password': password
            }).then(function(result){
                if(result['error'] == 'success'){
                    return window.open((window.location.origin + '/web'), "_self");
                }else{
                    self.$el.find('#error_msg_div').html(qweb.render('error_msg',{
                        'error': result['error']
                    }));
                }
            });
        },
        _OnSuperUserButton: function(e){
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var login_super = this.$el.find('#login').val();
            var password_super = this.$el.find('#password').val();
            ajax.jsonRpc('/web/become_login_popup', 'call', {'login': login_super, 'password': password_super
            }).then(function(result){
                if(result['error'] == 'success'){
                    return window.open((window.location.origin + '/web'), "_self");
                }else{
                    self.$el.find('#error_msg_div').html(qweb.render('error_msg',{
                        'error': result['error']
                    }));
                }
            });
        },
    });
});