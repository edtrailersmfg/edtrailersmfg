$(document).ready(function() {
    if($('#product_description_reviews').length){
        if($("#product_description_reviews").find('.nav.nav-tabs').find('li').length){
            if($("#product_description_reviews").find('.nav.nav-tabs').find('li').eq(0).find('a').length){
            var $target = $("#product_description_reviews").find('.nav.nav-tabs').find('li').eq(0).find('a');
                $target.addClass('active show');
                $('#product_description_reviews').find($target.attr('href')).addClass('active show');
            }
        }
    }
    });