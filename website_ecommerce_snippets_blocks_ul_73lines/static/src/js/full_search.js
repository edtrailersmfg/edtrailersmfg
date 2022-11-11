$(document).ready(function(){

var fullsearch_1 = document.querySelector('.close_btn');
if(fullsearch_1){
  fullsearch_1.addEventListener('click',hideSearch);
}

var fullsearch_2 = document.querySelector('.open_btn');
if(fullsearch_2){
  fullsearch_2.addEventListener('click',showSearch);
}

function showSearch() {
        $('#my_full_search').addClass('mystyle');
        $('header').addClass('nav_full_search');
}
function hideSearch() {
        $('#my_full_search').removeClass('mystyle');
        $('header').removeClass('nav_full_search');
}
});