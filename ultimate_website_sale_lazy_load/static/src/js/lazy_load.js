odoo.define("ultimate_website_sale_lazy_load.lazy_load", function(require){
    'use strict';

    var ajax = require('web.ajax');
    var ppg = 12;
    var offset = 0;
    var response = true;

    $(document).ready(function(){

        if($('#shop_lazy_load').length === 1){
            $('.pagination').remove();
            _renderContent();
        }

        async function scrollFunction(){
            if($('#wrapwrap').scrollTop() + $('#wrapwrap').height() > $('#shop_lazy_load').height() - 250) {
                await $("#wrapwrap").unbind('scroll');
                await _renderContent();
                return;
            }
        }

        async function _renderContent(){
            await renderSubContent();
            if(response){
                $("#wrapwrap").scroll( function(){
                    scrollFunction();
                });
            }
            return;
        }

        async function renderSubContent(){
            return ajax.jsonRpc('/get/shop/lazy_load','call',{
                'ppg': ppg,
                'offset': offset,
            }).then(function(data){
                if(data){
                    $('#shop_lazy_load').append(data);
                    offset = ppg + offset;
                    response = true;
                }else{
                    response = false;
                }
            });
        }

    });
});