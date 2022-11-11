$(document).ready( function(){
    if ($('.container').hasClass('oe_website_sale')){
        if($('.ecom-category-block').length){
            var elem = document.getElementsByClassName('ecom-category-block')[0];
            elem.scrollLeft = (elem.scrollWidth - elem.clientWidth) / 2;
            if(!($('.ecom-category-block')[0].scrollWidth != $('.ecom-category-block').width())){
                $('.ecom-category-block').addClass('justify-content-center');
            }
        }
    }
});



$('.brand-list-anchor-link').click(function(e){
  e.preventDefault();
  var target = $($(this).attr('href'));
  if(target.length){
    var scrollTo = target.offset().top;
    $('body, html').animate({scrollTop: scrollTo+'px'}, 800);
  }
});


$(document).ready( function(){
        $('[data-alphabet]:not(.disabled)').on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            var $target = $(e.currentTarget);
            $('[data-alphabet]').removeClass('active');
             $target.addClass('active');
             if($target.data('alphabet') != 'all'){
                $('[data-brand]').addClass('d-none');
                $('[data-brand="' + $target.data('alphabet') + '"]').removeClass('d-none');
             } else {
                $('[data-brand]').removeClass('d-none');

             }
        });
});