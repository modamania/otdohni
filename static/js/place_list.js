var Search = {
    init: function() {
        var time = $('.filter_work_time .input_time'),
            field = $('.filter_work_time .input_time input');
        
        this.timeout = false;
        this.time_selectors = $('#time_selectors');
        this.message = $('.js-search-message');
        this.button_reset_filter = $('#reset_filter');
        this.all_day = $('#all_day');
        this.from_time = $('#from_time');
        this.till_time = $('#till_time');
        this.sleep = 1000;

        this.check_all_day();

        this.from_time.timePicker();
        this.till_time.timePicker();
        this.bindUI();
    },

    bindUI: function(){
        var self = this;

        $('#time_switch_button').on('click', function() {
            var all_day = self.all_day_is_selected(),
                from_time = self.from_time.val(),
                till_time = self.till_time.val();

            if (all_day == true || from_time != '' || till_time != '')
                self.ajax_request();
        });

        $('.filter__selector').on('click', function(){
            self.ajax_request();
        });

        $('.input_time').find('input').each(function () {
            $(this).change(self.ajax_request);
        });

        // self.button_go
        //     .on('click', function(){
        //         self.button_go_click();
        //     });

        self.button_reset_filter
            .on('click', function(){
                self.reset_filter();
            });
        self.all_day
            .on('click', function(){
                self.change_all_day();
            });
    },

    unselect_selected_elements: function (name) {
        $('#'+name+'_list').find(".filter__selector.selected").each(function () {
            $(this).removeClass('selected');
        });
    },

    get_selected_elements: function (name) {
        arr = new Array();
        $('#'+name+'_list').find(".filter__selector.selected").each(function () {
            arr.push($(this).attr('data-'+name));
        });
        return arr;
    },

    gen_search_params: function() {
        var params = {};
        var tags = this.get_selected_elements('tag');
        if (tags.length){
            params.tag = tags;
        }

        var districts = this.get_selected_elements('district');
        if (districts.length){
            params.district = districts;
        }

        params.tsio = this.time_selectors.hasClass('invisible') === false ? 1 : 0;
        if (params.tsio){
            if (this.all_day_is_selected()) {
                params.all_day = 1;
            } else {
                params.from_time = this.from_time.val();
                params.till_time = this.till_time.val();
            }
        }

        params = $.param(params, true)
        return params
    },

    button_go_click: function () {
        var self = Search;

        params = self.gen_search_params();
        new_url = document.location.protocol + '//' + document.location.host + document.location.pathname + '?' + params + document.location.hash;
        document.location.replace(new_url);
    },

    run_ajax_request: function (method) {
        var self = Search;

        method = method || '';

        params = self.gen_search_params();
        new_url = document.location.protocol + '//' + document.location.host + '/api' + document.location.pathname + '?' + params + document.location.hash;
        t = $.getJSON(new_url, function (data){

            if (method != 'reset') {
                self.message
                    .text('Найдено ' + data.count + GetNoun(data.count, ' место', ' места', ' мест'));

                self.button_reset_filter
                    .toggleClass('hidden', (self.gen_search_params() == 'tsio=0'));
            }
        });

        Places.params = params;
        Places.getPlaces('replace');
    },

    ajax_request: function (method) {
        var self = Search;

        method = method || '';

        Places.catalog.addClass('places-catalog_state_loading');
        clearTimeout(self.timeout);
        self.timeout = setTimeout(function(){
             self.run_ajax_request(method);
            }, self.sleep);
    },

    reset_filter: function () {
        this.unselect_selected_elements('tag');
        this.unselect_selected_elements('district');
        this.all_day.attr('checked', false);
        this.check_all_day();
        this.from_time.val('');
        this.till_time.val('');
        this.ajax_request('reset');
        this.button_reset_filter.addClass('hidden');
        this.message.empty();
    },

    time_selectors_disable: function () {
        this.time_selectors.addClass('disabled');
        this.from_time.attr('disabled', 'disabled');
        this.till_time.attr('disabled', 'disabled');
    },

    time_selectors_enable: function () {
        this.time_selectors.removeClass('disabled');
        this.from_time.removeAttr('disabled');
        this.till_time.removeAttr('disabled');
    },

    all_day_is_selected: function () {
        if (this.all_day.is(':checked')) {
            return true;
        } else {
            return false;
        }
    },

    check_all_day: function () {
        if (this.all_day_is_selected()) {
            this.time_selectors_disable();
        } else {
            this.time_selectors_enable();
        }
    },

    change_all_day: function () {
        this.check_all_day();
        this.ajax_request();
    }
};

var Places = {
    templates: {
        placesItem: tmpl('<div class="places__item item" id="place-{%=o.id%}">'
            + '{% if (o.promo_is_up === "True") { %}<a title="{%=o.name%}" href="/places/{%=o.id%}/" class="thumb" {% if (o.photo) { %} style="background-image: url(/media/{%=o.photo%});"{% } %}>'
            + '{% if (!o.photo) { %}<span class="no_photo"></span>{% }%}'
            + '</a>{% } %}'
            + '<div class="place__summary">'
            + '<h3><a title="{%=o.name%}" href="/places/{%=o.id%}/">{%=o.name%}</a></h3>'
            + '<p class="tags">'
            + '{% for (var i=0, total = o.tagging.length; i<total; i++) { %}'
            +   '<a href="{%=o.tagging[i].url%}" title="{%=o.tagging[i].name%}">{%=o.tagging[i].name%}</a>{% if (i != (total - 1)) { %}, {% } %}'
            + '{% } %}'
            + '</p>'
            + '<div class="place-contact"><div class="place-contact__details">'
            + '<ul class="place-addresses">'
            + '{% for (var i=0, total = o.adr.length; i<total; i++) { %}'
            + '<li class="place-addresses__item">{% if (o.adr[i].lng && o.adr[i].lat) { %}<span class="js-toggle-address pseudo-link" data-index="{%= i.toString() %}" data-coord="[{%= o.adr[i].lat %}, {%= o.adr[i].lng %}]" >{%=o.adr[i].address%}</span>{% } else { %}{%=o.adr[i].address%}{% } %}{% if (o.adr[i].phone) { %}, тел.: {%=o.adr[i].phone%} {% } %}</li>'
            + '{% } %}'
            + '</ul>'
            + '</div><span class="js-toggle-contact place-contact__toggler pseudo-link">Адрес и телефон</span></div>'
            + '<div class="place__vote clearfix"><div class="commcount"><a href="/places/{%=o.id%}/#comments">{%=o.num_comments%}</a><i></i></div>'
            + '<div class="star-rating clearfix"><ol><li class="current-rating" style="width: {%=o.rating%}%;"></li></ol></div>'
            +'</div></div></div>'),
        baloonPlace: tmpl('<div class="place place_layout_baloon">'
            + '{% if (o.promo_is_up === "True") { %}<a title="{%=o.name%}" href="/places/{%=o.id%}/" target="_blank" class="thumb" {% if (o.photo) { %} style="background-image: url(/media/{%=o.photo%});"{% } %}>'
            + '{% if (!o.photo) { %}<span class="no_photo"></span>{% }%}'
            + '</a>{% } %}'
            + '<div class="place__summary">'
            + '<h3><a title="{%=o.name%}" href="/places/{%=o.id%}/" target="_blank">{%=o.name%}</a></h3>'
            + '<p class="tags">'
            + '{% for (var i=0, total = o.tagging.length; i<total; i++) { %}'
            +   '<a href="{%=o.tagging[i].url%}" title="{%=o.tagging[i].name%}">{%=o.tagging[i].name%}</a>{% if (i != (total - 1)) { %}, {% } %}'
            + '{% } %}'
            + '</p>'
            + '<ul class="place-addresses">'
            + '<li class="place-addresses__item">{%= o.address %}{% if (o.phone) { %}, {%= o.phone %}{% } %}</li>'
            + '</ul>'
            + '<div class="place__vote clearfix"><div class="commcount"><a href="/places/{%=o.id%}/#comments" target="_blank">{%=o.num_comments%}</a><i></i></div>'
            + '<div class="star-rating clearfix"><ol><li class="current-rating" style="width: {%=o.rating%}%;"></li></ol></div>'
            +'</div></div></div>')
    },
    placemarks: {
        base: {
            default: {
                iconLayout: 'default#image',
                iconImageHref: '/static/i/map/marker_sm.png',
                iconImageSize: [19, 19],
                iconImageOffset: [-5, -19]
            },
            active: {
                iconLayout: 'default#image',
                iconImageHref: '/static/i/map/marker_sm-active.png',
                iconImageSize: [19, 19],
                iconImageOffset: [-5, -19]
            }
        },
        promo: {
            default: {
                iconLayout: 'default#image',
                iconImageHref: '/static/i/map/marker.png',
                iconImageSize: [36, 35],
                iconImageOffset: [-11, -35]
            },
            active: {
                iconLayout: 'default#image',
                iconImageHref: '/static/i/map/marker-active.png',
                iconImageSize: [36, 35],
                iconImageOffset: [-11, -35]
            }
        }
    },
    init: function(options) {
        options = options || {};

        this.el = $('.js-places');
        this.catalog = $('.js-places-catalog');
        this.lastItem = this.catalog.find('.places__item').last();
        this.map_container = $('.js-places-map');
        this.list = $('.js-places-list');
        this.sorting = $('.js-places-sorting');
        this.perPage = options.perPage || 25;
        this.offset = 0;
        this.orderBy = 'default';
        this.params = Search.gen_search_params();

        this.getNextPage();
        this.bindUI();

        if (this.map_container.length) {
            this.stickMap();
            this.fitMap();

            ymaps.ready(function () {
                var geocode = ymaps.geocode(document.city);

                geocode.then(function (res) {
                    if (res.geoObjects.getLength()) {

                        geopoint = res.geoObjects.get(0).geometry.getCoordinates();
                        Places.map = new ymaps.Map("YMapsID", {
                                center: geopoint,
                                zoom: 11,
                                controls: ['zoomControl']
                            }
                        );
                        Places.setPlacemarks();
                    }
                });
            });
        }
    },

    bindUI: function() {
        var self = this;

        if (self.map_container.length) {
            $(window)
                .on('scroll', function(){
                    self.stickMap();
                })
                .on('resize', function(){
                    self.fitMap();
                    self.stickMap();
                });

            self.map_container
                .on('click', '.js-toggler', function(){
                    var $this = $(this),
                        altLabel = $this.data('alt-text');

                    $this.data('alt-text', $this.text()).text(altLabel);
                    self.toggleMap();
                })
                .on('click', '.js-close', function(){
                    self.closeMap();
                })
                .on('click', '.js-open', function(){
                    self.openMap();
                });
        }

        self.el
            .on('click', '.js-more-tags', function(){
                $(this).closest('.tags').addClass('tags_state_expanded');
            })
            .on('click', '.js-toggle-contact', function(){
                self.toggleContact($(this).closest('.places__item'));
            })
            .on('click', '.js-more-places', function(){
                self.renderPlaces(self.nextPageData);
                self.offset += self.perPage;
                self.getNextPage();
            })
            .on('click', '.js-toggle-address', function(){
                var item = $(this).closest('.places__item')[0];

                self.focusMap($(this).data('coord'), item, $(this).data('index'));
            });

        self.sorting
            .on('click', '.sorting__link', function(){
                var $this = $(this);

                if ($this.hasClass('sorting__link_state_active')) {
                    return;
                }

                $this.addClass('sorting__link_state_active')
                     .siblings()
                     .removeClass('sorting__link_state_active');

                self.orderBy = $this.data('orderBy')
                self.getPlaces('replace');
            });
    },
    stickMap: function() {
        var self = this,
            offset = self.el.offset(),
            minHeight = offset.top,
            maxHeight = self.list.outerHeight(),
            mapHeight = self.map_container.outerHeight(),
            y = window.scrollY,
            screenHeight = $(window).height(),
            top = (y >= minHeight) ? - Math.max(0, y - maxHeight - minHeight + screenHeight) : minHeight - y,
            lastItemHeight = (self.lastItem.length) ? self.lastItem.outerHeight() : $('.places__item').last().outerHeight(),
            isStatic = mapHeight >= maxHeight;

        self.map_container
            .toggleClass('sticky', y >= minHeight)
            .css({
                left: (y >= minHeight) ? (offset.left + self.catalog.outerWidth(true)) : self.catalog.outerWidth(true),
                bottom: (y >= minHeight) ? Math.max(0, y - maxHeight - minHeight + screenHeight) : 'auto',
                height : (y >= minHeight) ? 'auto' : screenHeight - offset.top + y
            });

        if (y >= minHeight + maxHeight - lastItemHeight) {
            self.map_container.css({
                top: (minHeight + maxHeight - lastItemHeight) - y,
                height: lastItemHeight
            });
        } else {
            self.map_container.css({
                top: ''
            });
        }

        this.catalog.css({
            minHeight: (this.map_container.is(':visible')) ? this.map_container.outerHeight() : 0
        });

        if (self.map){
            self.map.container.fitToViewport();
        }
    },
    unstickMap: function() {
        var self = this,
            maxHeight = self.list.outerHeight(),
            mapHeight = self.map_container.outerHeight();

        self.map_container
            .addClass('static')
            .css({
                top : 0,
                left: 'auto',
                bottom: 0,
                height: (maxHeight > 0) ? maxHeight : mapHeight,
                width : self.el.outerWidth() - self.catalog.outerWidth(true)
            });

        this.catalog.css({
            minHeight: (this.map_container.is(':visible')) ? this.map_container.outerHeight() : 0
        });

        if (self.map) {
            self.map.container.fitToViewport();
        }
    },
    fitMap: function() {
        var offset = this.el.offset(),
            catalogWidth = this.catalog.outerWidth(true)

        this.map_container
            .css({
                width : this.el.outerWidth() - catalogWidth,
                left: (this.map_container.is('.sticky')) ? offset.left + catalogWidth : catalogWidth
            });

        this.catalog.css({
            minHeight: (this.map_container.is(':visible')) ? this.map_container.outerHeight() : 0
        });

        if (this.map){
            this.map.container.fitToViewport();
        }
    },
    focusMap: function(coords, item, index){
        var self = this;

        if (typeof coords != 'undefined') {
            self.map.panTo([coords]).then(function(){
                Places.map.setCenter(coords, 16);
                if (item.Placemarks.length) {
                    item.Placemarks[index].balloon.open();
                }
            });

        }
    },
    openMap: function(){
        this.el.removeClass('places_map_collapsed');
        this.fitMap();
        this.stickMap();
    },
    closeMap: function() {
        this.el.addClass('places_map_collapsed');
        this.fitMap();
    },
    toggleMap: function() {
        this.el.toggleClass('places_map_expanded');
        this.stickMap();
        this.fitMap();
    },
    toggleContact: function(place) {
        place.find('.place-contact')
             .addClass('place-contact_state_expanded');
    },
    highlightPlacemark: function() {
        if (this.Placemarks.length) {
            $.each(this.Placemarks, function(index, placemark){
                if (placemark.isPromo) {
                    placemark.options.set(Places.placemarks.promo.active);
                } else {
                    placemark.options.set(Places.placemarks.base.active);
                }
            });
        }
    },
    unHighlightPlacemark: function() {
        if (this.Placemarks.length) {
            $.each(this.Placemarks, function(index, placemark){
                if (placemark.isPromo) {
                    placemark.options.set(Places.placemarks.promo.default);
                } else {
                    placemark.options.set(Places.placemarks.base.default);
                }
            });
        }
    },
    highlightPlace: function(el) {
        el.addClass('places__item_state_hover')
          .siblings()
          .removeClass('places__item_state_hover');
    },
    enableMoreButton: function(){
        $('.js-more-places').removeClass('hidden');
    },
    resetMoreButton: function(){
        $('.js-more-places').addClass('hidden');
    },
    resetOffset: function(){
        this.offset = 0;
    },
    getURL: function(params){
        var params = params || document.location.search.replace('?',''),
            url = document.location.protocol
                       + '//' + document.location.host
                       + '/api/json'
                       + document.location.pathname
                       + '?' + params
                       + document.location.hash;
        return url;
    },
    getPlaces: function(method){
        var self = this,
            method = method || 'append',
            url = this.getURL('order_by=' + this.orderBy + '&' + this.params);


        $.getJSON(url, function(data) {
            if (method === 'replace') {
                self.resetOffset();
                self.catalog.removeClass('places-catalog_state_loading');
            }

            self.renderPlaces(data, method);
            self.getNextPage();
        });
    },
    renderPlaces: function(data, method) {
        var self = this,
            templates = self.templates,
            placesList = '',
            container = self.el.find('.places__item-list');

        self.map_container.toggleClass('hidden', !data.length);

        if (data.length) {
            $.each(data, function(index, place) {
                placesList += templates.placesItem(place);
            });

            if (method === 'replace') {
                container.html(placesList);
            } else {
                container.append(placesList);
            }
            self.lastItem = self.catalog.find('.places__item').last();
            self.fitMap();
            self.stickMap();
            self.renderPlacemark(data, method);
        } else {
            self.catalog.css({
                minHeight: 0
            });
            container.html('<p>К сожалению, по выбранным параметрам ничего не найдено, попробуйте изменить настройки или сбросить фильтр. Мы уверены, вы найдёте отличное место!</p>')            
        }
    },
    getNextPage: function(){
        var self = this,
            offset = this.offset + this.perPage,
            url = this.getURL('offset=' + offset + '&' + 'order_by=' + this.orderBy + '&' + this.params);
            jqxhr = $.getJSON(url, function(data){
                        self.nextPageData = data;
                        self.enableMoreButton();

                        if (!data.length) {
                            self.resetMoreButton();
                        }
                    });
    },
    setPlacemarks: function() {
        var url = this.getURL();

        $.getJSON(url, function (data) {
            Places.renderPlacemark(data);
        });
    },
    renderPlacemark: function(data, method) {
        
        var self = this,
            clusterer = new ymaps.Clusterer({
                preset: 'twirl#invertedVioletClusterIcons',
                groupByCoordinates: false
            }),
            method = method || 'append';

        if (method == 'replace')    
            self.map.geoObjects.removeAll();

        // geoObjects = [];
        // Разделить этот каскад циклов на разные функции
        // Использовать $.proxy для передачи this

        $.each(data, function(index, place) {

            var hasPromo = (place.promo_is_up == 'True'),
                marker = (hasPromo) ? Places.placemarks.promo.default : Places.placemarks.base.default;

            $.each(place.adr, function (index, address) {
                geopoint = [parseFloat(address.lat), parseFloat(address.lng)];

                if (geopoint[0] && geopoint[1]) {
                    place.address = address.address;
                    place.phone = address.phone;

                    var address_placemark = new ymaps.Placemark(geopoint,
                        {
                            // balloonContent: '<h3>' + place.name + '</h3>' + address.address
                            balloonContent : self.templates.baloonPlace(place)
                        },
                        marker),
                        placeEl = document.getElementById('place-' + place.id);

                    address_placemark.isPromo = hasPromo;

                    if (placeEl) {
                        var $placeEl = $(placeEl);
                        
                        if (typeof placeEl.Placemarks == 'undefined') {
                            placeEl.Placemarks = [];
                        }

                        placeEl.Placemarks[index] = address_placemark;

                        $placeEl.hover(self.highlightPlacemark, self.unHighlightPlacemark);

                        address_placemark.events.add('click', function(){
                            self.highlightPlace($placeEl);

                            $('html, body').animate({
                                scrollTop: $placeEl.offset().top + ($placeEl.outerHeight() / 2) - (window.innerHeight / 2)
                            }, 500);
                        });
                    }
                    Places.map.geoObjects.add(address_placemark);
                    // geoObjects.push(address_placemark);
                }
            });
        });
        // clusterer.add(geoObjects);
        
        // Places.map.geoObjects.add(clusterer);
    }
};

$(function(){

    Search.init();
    Places.init();

    $("#search_place").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/api/places/search/",
                dataType: "json",
                data:{
                    t: request.term,
                    path: document.location.pathname
                },
                success: function (data){
                    response(data.names);
                }
            });
        },
        minLength: 1
    });

});
