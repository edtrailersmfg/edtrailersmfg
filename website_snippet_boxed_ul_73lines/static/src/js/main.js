(function ($) {
    // USE STRICT
    "use strict";
    $.fn.counters = function(options) {
        return this.each(function() {
            var container = $(this),
                elements = container.find('.count_to .odometer');
            //trigger displaying of thumbnails
            container.appear(function() {
                elements.each(function(i) {
                    var $count = $(this);
                    var od = new Odometer({
                        el: $count[0],
                        format: '',
                        theme: 'minimal',
                        duration: $count.data('duration')
                    });
                    od.update($count.data('number'));
                });
            });
        });
    };
    $.fn.animate_on_appear = function(options_passed){
        return this.each(function(){
            var self = $(this);
            self.appear( function(){
                var effect = $(this).data('animation');
                var delay = $(this).data('delay');
                $(this).delay(delay).queue( function() {
                $(this).removeClass('with_animation').addClass( effect );
               });
            });
        });
    };
    $.fn.chart_skill = function(options){
        return this.each(function(){
            var container = $(this), elements = container.find('.chart');
            //trigger displaying of thumbnails
            container.appear(function(){
                elements.each(function(i){
                    var $chart = $(this);
                    var color = $(this).data('color');
                    var color2 = $(this).data('color2');
                        $chart.easyPieChart({
                            lineWidth: 8,
                            size: 140,
                            trackColor: color2,
                            scaleColor: false,
                            barColor: color,
                            barColor2: color,
                            animate:2000
                        });
                });
            });
        });
    }
    /* ----------------------------- Fullscreen Section ---------------------- */

})(jQuery);


$(document).ready(function () {
    if($('[data-snippet="s_presentation_page"]').length){
        $('#wrapwrap').css({'overflow': 'hidden'});
    }
    if($.fn.chart_skill)
    {
        $('.chart_skill').chart_skill();
    }
    if($.fn.counters)
    {
        $('.state-col-inner').counters();
    }

//   skill chart js
    $('.chart_skill > .chart > span').bind("DOMSubtreeModified",function(ev){
        ev.target.parentNode.setAttribute('data-percent', ev.target.innerText);
    });
    (function() {
	"use strict";
	/*[pan and well CSS scrolls]*/
	var pnls = document.querySelectorAll('.panel').length,
		scdir, hold = false;

	function _scrollY(obj) {
		var slength, plength, pan, step = 100,
			vh = window.innerHeight / 100,
			vmin = Math.min(window.innerHeight, window.innerWidth) / 100;
		if ((this !== undefined && this.id === 'well') || (obj !== undefined && obj.id === 'well')) {
			pan = this || obj;
			plength = parseInt(pan.offsetHeight / vh);
		}
		if (pan === undefined) {
			return;
		}
		plength = plength || parseInt(pan.offsetHeight / vmin);
		slength = parseInt(pan.style.transform.replace('translateY(', ''));
		if (scdir === 'up' && Math.abs(slength) < (plength - plength / pnls)) {
			slength = slength - step;
		} else if (scdir === 'down' && slength < 0) {
			slength = slength + step;
		} else if (scdir === 'top') {
			slength = 0;
		}
		if (hold === false) {
			hold = true;
			pan.style.transform = 'translateY(' + slength + 'vh)';
			setTimeout(function() {
				hold = false;
			}, 1000);
		}
		console.log(scdir + ':' + slength + ':' + plength + ':' + (plength - plength / pnls));
	}
	/*[swipe detection on touchscreen devices]*/
	function _swipe(obj) {
		var swdir,
			sX,
			sY,
			dX,
			dY,
			threshold = 100,
			/*[min distance traveled to be considered swipe]*/
			slack = 50,
			/*[max distance allowed at the same time in perpendicular direction]*/
			alT = 500,
			/*[max time allowed to travel that distance]*/
			elT, /*[elapsed time]*/
			stT; /*[start time]*/
		obj.addEventListener('touchstart', function(e) {
			var tchs = e.changedTouches[0];
			swdir = 'none';
			sX = tchs.pageX;
			sY = tchs.pageY;
			stT = new Date().getTime();
			//e.preventDefault();
		}, false);

		obj.addEventListener('touchmove', function(e) {
			e.preventDefault(); /*[prevent scrolling when inside DIV]*/
		}, false);

		obj.addEventListener('touchend', function(e) {
			var tchs = e.changedTouches[0];
			dX = tchs.pageX - sX;
			dY = tchs.pageY - sY;
			elT = new Date().getTime() - stT;
			if (elT <= alT) {
				if (Math.abs(dX) >= threshold && Math.abs(dY) <= slack) {
					swdir = (dX < 0) ? 'left' : 'right';
				} else if (Math.abs(dY) >= threshold && Math.abs(dX) <= slack) {
					swdir = (dY < 0) ? 'up' : 'down';
				}
				if (obj.id === 'well') {
					if (swdir === 'up') {
						scdir = swdir;
						_scrollY(obj);
					} else if (swdir === 'down' && obj.style.transform !== 'translateY(0)') {
						scdir = swdir;
						_scrollY(obj);

					}
					e.stopPropagation();
				}
			}
		}, false);
	}
	/*[assignments]*/
	var well = document.getElementById('well');
	if(well){
        well.style.transform = 'translateY(0)';
        well.addEventListener('wheel', function(e) {
            if (e.deltaY < 0) {
                scdir = 'down';
            }
            if (e.deltaY > 0) {
                scdir = 'up';
            }
            e.stopPropagation();
        });
        well.addEventListener('wheel', _scrollY);
        _swipe(well);
        var tops = document.querySelectorAll('.top');
        for (var i = 0; i < tops.length; i++) {
            tops[i].addEventListener('click', function() {
                scdir = 'top';
                _scrollY(well);
            });
        }
	}
})();

});