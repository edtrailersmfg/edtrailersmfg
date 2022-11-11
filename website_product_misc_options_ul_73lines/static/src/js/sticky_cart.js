$(document).ready( function(){
    $('#wrapwrap').scroll(function(){
        if ($(this).scrollTop() > 100) {
           $('.sticky-product-cart').addClass('sticky-product-cart-show');
        } else {
           $('.sticky-product-cart').removeClass('sticky-product-cart-show');
        }
    });
});