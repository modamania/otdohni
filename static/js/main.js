(function($) {
    $.fn.exists = function() {
   return $(this).length;
}
})(jQuery);

var sliderOptions = function(){
    return {
        minSlides: 1,
        maxSlides: 3,
        slideWidth:  getSlideWidth(),
        slideMargin: 0,
        pager: false,
        auto: true,
        autoHover: true,
        pause: 5000
    }
};

function getSlideWidth() {
    var contentWidth = $('.content').width();
    return $(window).width() > 1200 ? contentWidth / 2.3 : contentWidth / 1.5;
}

function get_category(){
    // get active category of filters
    var url = $('.event_types__type_active input').attr('value');
    if (!url){
        url = $('#event__base__url').attr('value');
    }
    if (url && url[url.length - 1] == '/'){
        url = url.slice(0, url.length - 1);
    }
    return url;
}

function set_active_day(){
    var input = $('#event__active__day').attr('value');
    if (input){
        var match = /(\d{4})\/(\d{1,2})\/(\d{1,2})/.exec(input);
        if (match[3] < 10){
            match[3] = match[3].slice(1);
        }
        var day = match.slice(1).join('/');
        $("td a[href$='" + day + "']").addClass('active__day');
    };
};

function initSlider(){
    var eventsList = $('.events__item-list');

    $.each(eventsList, function(){
        var $this = $(this),
            slider = $this.data('slider') || '';

        if (slider) {
            slider.reloadSlider(sliderOptions());
            return;
        }

        if ($this.children().length > 1) {
            slider = $this.bxSlider(sliderOptions());

            $this.data('slider', slider);
        }
    });
}

var JumpUp = {
    el : $('.jump-up'),
    init : function(){
        this.bindUI();
        setTimeout(function(){
            JumpUp.togglePosition();
        }, 1000);
    },
    bindUI : function() {
        var self = this;

        self.el.on('click', function(){
            $('html, body').animate({
                scrollTop: 0
            }, 500);
        });

        $(window).on('scroll', function(){
            self.togglePosition();
        });
    },
    togglePosition : function(){
        var self = this,
            y = $(window).scrollTop(),
            windowHeight = $(window).height(),
            aside = $('.aside');

        self.el
            .toggleClass('jump-up_pos_fixed', y > aside.offset().top + aside.outerHeight() - windowHeight + self.el.height())
            .css({
                marginBottom : Math.max(0, y - $('.footer').offset().top + windowHeight - self.el.height()/2)
            });
    }
}

$(function(){
    JumpUp.init();
});

$(function(){
    $('.aside-toggler').on('click', function(){
        $('.page').toggleClass('page_state_pushed');
        
        if (typeof Places !== 'undefined') {
            Places.fitMap();
        }
    });
});

$(function(){
    calendar = new Calendar();
    var prefix = $('#event__base__url').attr('value');
    calendar.create(prefix);
});

$(function(){
    $('.schedule__calendar').on('click', function(){
        $('#calendar_filter_base').toggleClass('calendar_state_visible');
    })
});


$(function(){
    var category = get_category();
    var pattern = new RegExp("(\\d{4,}/\\d{1,2}/\\d{1,2})")
    $('#calendar_filter_parent table a').live('click', function(){
        var url = $(this).attr('href')
        var match = pattern.exec(url)
        $(this).attr('href', [category, match[1]].join('/'))
    });
});

$(function(){
    var selectedType = $(':selected','#id_category').val();
    if (selectedType==14) {
      $('#movie_info').show();
    } else if (selectedType==24) {
      $('#show_info').show();
    } else {
      $('#any_info').show();
    }

    $("#id_category").change(function () {
        var selectedType = $(':selected','#id_category').val();
        if (selectedType==14) {
          $('#movie_info').fadeIn(300);
          $('#any_info').hide();
          $('#show_info').hide();
        } else {
          $('#movie_info').hide();
          $('#any_info').show();
        }

        if (selectedType==24) {
          $('#show_info').fadeIn(300);
          $('#any_info').hide();
        } else {
          $('#show_info').hide();
        }
    });
});

$(function(){
  $('#head_search').myautocomplete({
    'url_for_ajax': "/api/search/",
    'prefix_for_url_all_result': '/api/search?t='
  });

  $('#search_field').myautocomplete({
    'url_for_ajax': "/api/search/",
    'prefix_for_url_all_result': '/api/search?t='
  });
});

$(function(){
    // scrolling the calendar in the filter
    set_active_day()
    $('#calendar_prev_month, #calendar_next_month').live('click', function(){
        var url = $(this).attr('href');
        var self = this;
        $.get(url, function(data){
            $(self).parent().replaceWith(data);
            set_active_day()
        });
        // add class for active day
        return false;
    });
});

$(function(){
    $('.afisha .tabs-item').on('click', function(e){
        e.stopPropagation();

        var self = $(this),
            loading = $('<span class="loading"/>'),
            update_holder = self.parents('.afisha_index').find('.afisha__content');

        if(!self.find('.loading').length) {
            self.append(loading);
        }

        self
            .addClass('tabs-item_state_current')
            .siblings()
                .removeClass('tabs-item_state_current');

        $.ajax({
            url: '/',
            type: "GET",
            data: self.data('period') + '=' + self.data('category'),
            success: function(context) {
                update_holder.html( context );
                
                var list = update_holder.find('.events__item-list');

                if (list.children().length > 1) {
                    list.bxSlider(sliderOptions());                    
                }

                loading.remove();
            },
            error:  function(context, error){
                update_holder.html(error);
            }
        });
     });
});

$(function(){
    initSlider();

    $(window).on('resize', function(){
        initSlider();
    });
});

$(function(){
    $(".like-button").click(function () {
        var $this = $(this),
            uri = $(this).find('a').attr('href'),
            link = $(this),
            status = $this.parents('.nominies__likes'),
            works_container = $this.parents('.nominies__item-list');

        $this.parent().addClass('ajax');
        status.replaceWith('<p class="current-votes">Спасибо за Ваш голос!</p><br>');
        if (works_container.data('tochoose') == 'one')
            works_container.find('.like-button').remove();

        $.post(
            uri,
            {'data':uri},
            function(data) {
                status.replaceWith(data);
                link.show().parent().removeClass('ajax');
            }, 'html');
        return false;
    });
});

$(function(){
	$('span#pseudo_film').click(function(){
		$('div#calendar_film_base').toggle(800);
	})
});

$(function(){
    $('#calendar_arr').dateinput();
    $('#toggle_calendar').on('click', function(){
       $('#calendar_base').toggleClass('calendar_state_visible');
    });
});

$(function(){
    $(".infield label").inFieldLabels({fadeOpacity: 0});
    $("a[rel=lightbox], a[rel=fancybox], a.fancybox").fancybox({ autoScale: false});
});

$(function() {
    $("ul.fotoreports__tabs").tabs(".fotoreports__content");
    $("ul[class*='afisha']").tabs(".events__content");
    $("ul.tabs-days").tabs(".event__schedule",{
        tabs : 'li',
        current: 'tabs-item_state_current'
    });
});

$(function() {
    $("#tagcloud_popup_trigger, #tagcloud_close").on('click', function(){
        $('.tagcloud_popup').toggleClass('hidden');
    });
});

$(function(){
    $('#w-new-places').bxSlider({
        controls: false,
        auto: true
    });
});

$(function(){
    $('#buy_tickets_modal').detach()
        .appendTo('body');
        
    $('.tour-steps').bxSlider({
        controls: true,
        auto: false
    });
});



/*
* Show first 10 items in navigation widget
*/

/*$(function(){
    var navWidgets = $('.widget_nav');
    
    $.each(navWidgets, function(){
        var self = $(this),
            navWidgetsItems = $(this).find('ul li');      

        if (navWidgetsItems.length >= 10) {
            navWidgetsItems.filter(':nth-child(n+10)').hide();
            self.append('<span class="widget_nav__more dropdown"><span class="pseudo-link">еще</span></span>')
        }
    });


    navWidgets.on('click', '.widget_nav__more', function(e){
        $(this).remove();
        $(e.delegateTarget).find('ul li').show();
    });
});*/

(function($) {
    switch_tab = function (o) {
        $this = $(o);
        $this.addClass('tabs-item_state_current').siblings().removeClass('tabs-item_state_current')
            .parents('.tabbed').find('.pane').hide().eq($this.index()).fadeIn(150).trigger('show.tab');
        }
    $(function() {
        if (window.location.hash !== ''){
            hash = document.location.hash.replace('#', '').split('-')[0];
            $('.tabbed .tabs-item[data-tabname='+hash+']').each(function () {
                switch_tab(this);
            });
        };
        $('.tabbed').on('click', '.tabs-item:not(.tabs-item_state_current)', function() {
            $this = $(this);
            if ($this.data('tabname')) {
                document.location.hash = $this.data('tabname');
                switch_tab(this);
            }

            if (typeof Places !== 'undefined') {
                Places.fitMap();
            }
        })
    })
})(jQuery);

$(function(){
    $('.filter__selector').click(function(){
        $(this).toggleClass('selected');
    });
});


(function ($, F) {
    F.transitions.dropIn = function() {
        var endPos = F._getPosition(true);

        endPos.top = (parseInt(endPos.top, 10) - 200) + 'px';

        F.wrap.css(endPos).show().animate({
            top: '+=200px'
        }, {
            duration: F.current.openSpeed,
            easing: 'easeOutBounce',
            complete: F._afterZoomIn
        });
    };

    F.transitions.dropOut = function() {
        F.wrap.removeClass('fancybox-opened').animate({
            top: '-=200px',
            opacity: '0'
        }, {
            duration: F.current.closeSpeed,
            complete: F._afterZoomOut
        });
    };

}(jQuery, jQuery.fancybox));

$(function(){
    jQuery("#more_links_button").popup({
        container: '.profile-dropdown'
    });
});

$(function(){
    $('.comment_form, .comments__comment').comment_form();
    $('.comment__rating').comment_rating();
});

var NewsBlock = {
    options: {
        'container' : '.latest-news',
        'timeout' : 5E3,
        'fadeTime' : 300,
        'itemClass' : 'news-leads-item',
        'currentClass' : 'news-leads-item_state_current'
    },
    init: function(){
        this.news = $(this.options.container);
        this.caption = this.news.find('.news-thumb__caption');
        this.thumb = this.news.find('.news-thumb');
        this.leads = this.news.find('.news-leads');

        this.news.on('mouseenter', '.' + this.options.itemClass, function(){
            NewsBlock.swap($(this));
            NewsBlock.stop();
        });

        this.news.on('mouseleave', '.' + this.options.itemClass, function(){
            /*NewsBlock.start();*/
        });

        NewsBlock.start();
    },
    swap: function(item){
        var o = this;

        if (item.hasClass(o.options.currentClass)) {
            return;
        }

        item
            .siblings()
            .removeClass(o.options.currentClass)
            .end()
            .addClass(o.options.currentClass);

        o.thumb
            .fadeOut(o.options.fadeTime, function(){
                    $(this)
                        .css('backgroundImage', "url(" + item.find('.' + o.options.itemClass + '__img').attr('src') +")")
                        .fadeIn(o.options.fadeTime);
            });

        o.caption
            .fadeOut(o.options.fadeTime, function(){
                $(this)
                    .html(item.find('.' + o.options.itemClass + '__summary').html())
                    .fadeIn();
            })
    },
    swapToNext: function(){
        var o = this,
            current = o.leads.find('.' + o.options.currentClass),
            next;
        
        if ((current).is(':last-child')) {
            next = o.leads
                        .find('.' + o.options.itemClass)
                        .first();
        } else {
            next = current.next();
        }

        NewsBlock.swap(next);
    },
    start: function(){
        this.timer = setInterval(function(){
            NewsBlock.swapToNext();
        }, this.options.timeout);
    },
    stop: function(){
        clearInterval(this.timer);
    }
};

NewsBlock.init();

$(function(){
    $('.show-help').on('click', function(e){
        e.stopPropagation();

        var self = $(this),
            title = self.closest('h1'),
            x = self.position().left + self.outerWidth(),
            y = title.position().top + parseInt(title.css('marginTop'));

        if (self.hasClass('active')){
            self.removeClass('active');
            hideHelp();
        } else {
            self.addClass('active');
            showHelp(x,y);            
        }
     });

    $('.tooltip_type_help').on('click', '.tooltip-close', function(){
        hideHelp();
    });
});

function showHelp(x,y){
    $('.tooltip_type_help')
        .css({
            top: y,
            left: x
        })
        .addClass('tooltip_state_visible');
    $(document)
    .on('click', '.tooltip', function(e){
        e.stopPropagation();
    })
    .on('click.tooltip', function(){
        hideHelp();
    });
}

function hideHelp(){
    $('.show-help').removeClass('active');
    $('.tooltip_type_help').removeClass('tooltip_state_visible');
    $(document).off('click.tooltip');
}

/* Демо скрипты */

$(function(){
    var field = $(".upload__field input");
    var popup = $(".upload__popup");

    $(".input__file .pseudo_link").click(function(){
        $(this).next().toggle();
    });

    // for current photo
    $(".upload__thumb").click(function(){
    })

    field.change(function(){
       $(this).parent().parent().addClass('fieldset_load');
       $('.upload__popup').show();
   });

   $('.upload__popup .cancel_button').click(function(){
       $('.upload__popup').hide();
   });
});

function getscroll(){
    if (self.pageYOffset){
        yScroll = self.pageYOffset;
        xScroll = self.pageXOffset;
    } else if (document.documentElement && document.documentElement.scrollTop){
        yScroll = document.documentElement.scrollTop;
        xScroll = document.documentElement.scrollLeft;
    } else if (document.body){
        yScroll = document.body.scrollTop;
        xScroll = document.body.scrollLeft;
    }
};

(function($) {

    var defaults = {
        droplistShow : function(e) {
           var wrapper =  $('<div class="dropdown__popup" />').click(function(e){e.stopPropagation();});
           var self = this;
           this.data('popupVisible', true);
           var popupVisible = this.data('popupVisible');
           self.wrap(wrapper);
           $(document).bind('click.droplist', function (e) {
                self.hide_on_click(e);
            });
           $(document).bind('keyup.droplist', function (e) {
                self.hide_on_keypress(e);
            });
        },
        droplistHide : function() {
            this.parent().replaceWith(this.parent().contents());
            this.data('popupVisible', false);
            $(document).unbind('.droplist');
        },
        hide_on_click : function (e) {
            var popupVisible = this.data('popupVisible');
            if (popupVisible) {
                this.droplistHide();
            }
            return self;
        },
        hide_on_keypress : function (e) {
            var self = this;
            switch (e.keyCode) {
                case 27:
                    self.droplistHide();
                    break;
            }
            return self;
        }
    };

    var methods = {
        init : function(options){
            return this.each(function () {
                var options = $.extend({}, defaults, options);
                var list = $(this);
                list.droplistShow = options.droplistShow;
                list.droplistHide = options.droplistHide;
                list.hide_on_click = options.hide_on_click;
                list.hide_on_keypress = options.hide_on_keypress;
                var holster = list.find('.dropdown__visible').bind('click.droplist', function(e){
                    list.droplistShow();
                    e.stopPropagation();
                });
                var item = list.find('.dropdown__item');

                item.each(function () {
                    var item = $(this);
                    item.wrapInner('<span class="pseudo-link" />');
                });

                var link = item.find('.pseudo-link').bind('click.droplist',function(){
                   var self = $(this).parent();
                   holster.html(self.html());
                   self.prependTo(self.parent());
                   list.droplistHide();
                });
                $(this).data('popupVisible', false);
                $(this).data('list', list);
            });
        }
    }

    $.fn.droplist = function(method){
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method "' +  method + '" not fined in jQuery.droplist' );
        }
    };

})(jQuery);

GetNoun = function(number, one, two, five) {
    number = Math.abs(number);
    number %= 100;
    if (number >= 5 && number <= 20) {
        return five;
    }
    number %= 10;
    if (number == 1) {
        return one;
    }
    if (number >= 2 && number <= 4) {
        return two;
    }
    return five;
}

GetAdj = function(number, one, two) {
    number %= 100;
    if (number == 11) return two;
    number %= 10;
    if (number == 1) return one;
    return two;
}


$(function(){
    var wolf = $('.wolf'),
        slides = wolf.find('.wolf__slide'),
        slideshow = (slides.length > 1) ? true : false;

    if (!slides.filter('.activeslide').length) {
        slides
            .first()
            .addClass('activeslide');
    }

    if (slideshow){
        var slideshow_interval = setInterval(function(){
            toggleWeather(slides);
        }, 8000);
    }
});

function toggleWeather(slides) {
    var slides = slides,
        currentslide = slides.filter('.activeslide'),
        nextslide,
        prevslide;

    if($.inAnimation) {
        return;
    } else {
        $.inAnimation = true;
    }

    currentslide
        .removeClass('activeslide');

    if ( currentslide.length == 0 ) {
        currentslide = slides[-1];
    }

    nextslide = currentslide.next().length ? currentslide.next() : slides.first();
    prevslide =  nextslide.prev().length ? nextslide.prev() : slides.last();
    $('.prevslide')
        .removeClass('prevslide');
    prevslide
        .addClass('prevslide');
    nextslide
        .hide()
        .addClass('activeslide');
    nextslide
        .fadeIn('slow', function(){
            $.inAnimation = false;
        });
    prevslide
        .fadeOut('slow', function(){
            $.inAnimation = false;
        });
}

$(function(){
    $('.toggle-winner-info').on('click', function(e){
        e.preventDefault();

        var $this = $(this),
            cards = $('.actions-winners__item'),
            fullInfo = $('.winner-info'),
            winner = $this.parents('.actions-winners__item');

        fullInfo
            .find('.winner-info__thumb').attr('src', winner.find('.photo-link').attr('href'))
            .end()
            .find('.winner-info__name').text(winner.find('.winner__name').text())
            .end()
            .find('.winner-info__quote').text(winner.find('.winner__quote').text())
            .end()
            .find('.winner-info__title').text(winner.find('.action-title').text())
            .end()
            .find('.winner-info__date').text(winner.find('.date').text());

        winner
            .toggleClass('is-active')
            .siblings()
            .removeClass('is-active');

        var cardsTotal = cards.length,
            cardsPerRow = Math.floor($('.content').width() / winner.width()),
            currentRow = Math.ceil((winner.index() + 1) / cardsPerRow),
            index = (cardsTotal > currentRow * cardsPerRow) ? (currentRow * cardsPerRow ) : 0;

        fullInfo
            .insertAfter(cards.eq(index - 1))
            .before('  ')
            .after(' ')
            .toggleClass('hidden', !winner.is('.is-active'));

        $('html, body').animate({
            scrollTop: winner.offset().top - 40
        }, 500);

    });

    $(window).on('resize', function(){
        var cards = $('.actions-winners__item'),
            fullInfo = $('.winner-info'),
            winner = cards.filter('.is-active'),
            cardsTotal = cards.length,
            cardsPerRow = Math.floor($('.content').width() / winner.width()),
            currentRow = Math.ceil((winner.index() + 1) / cardsPerRow),
            index = (cardsTotal > currentRow * cardsPerRow) ? (currentRow * cardsPerRow ) : 0;

        fullInfo
            .insertAfter(cards.eq(index - 1))

    });

    $('.winner-info').on('click', '.popup__close', function(e){
        $(e.delegateTarget).toggleClass('hidden');
        $('.actions-winners__item.is-active').toggleClass('is-active');
    });
});

$(function(){
    var b3 = $('.rkb-third');
    if (b3.length) {
        $(window).on('load', function(){
            var offset = b3.offset();
            $(window).on('scroll', function(){
                var top = $(this).scrollTop();
                b3.toggleClass('rkb-third_pos_fixed', top > offset.top);
            });
        });
    }
});

$(function(){
    $('.js-filter').on('click', '.js-filter-option', function(e){
        var $this = $(this),
            active = 'filter-option_state_active',
            currentValue = $this.data('value'),
            filter = $(e.delegateTarget)
            options = filter.find('.js-filter-option').not($this),
            target = $('.' + filter.data('target'));

        $this.addClass(active);
        target.addClass(currentValue);

        $.each(options, function(index, option){
            var $option = $(option);

            $option.removeClass(active);
            target.removeClass($option.data('value'));
        });
    });
});

$(function(){
    $('.js-profile-stats').on('click', '.js-profile-stats-toggler', function(e){
        var tabname = $(this).data('tab');
        document.location.hash = tabname;
        $('.tabbed .tabs-item[data-tabname='+tabname+']').each(function () {
            switch_tab(this);
        });
    });
});