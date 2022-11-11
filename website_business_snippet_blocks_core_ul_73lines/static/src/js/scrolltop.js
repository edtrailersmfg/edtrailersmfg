//Hide Back To Top Button When Page Scroll Is 0

$("#o_footer_scrolltop").hide();
//fade in #back-top
$(document).ready(function () {
    $('#wrapwrap').scroll(function() {
      if ($(this).scrollTop() > 100) {
         $('#o_footer_scrolltop_wrapper').addClass("show");
      } else {
         $('#o_footer_scrolltop_wrapper').removeClass("show");
      }
    });
    $(".ultimate_scrolltop a").on("click", function (e) {
        return e.preventDefault(), $("#wrapwrap").animate({ scrollTop: 0 }, 1000), !1;
    });
});
