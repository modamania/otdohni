(function () {
    var ps = {}

    function getGeopointByAddress() {
        var value = ps.address;
        v = value.split('/');
        try {
            re = /^\w*\d+/ig
            var v1 = re.test(v[1]);
            if (v1 == false){
                value = v[0];
            }
        } catch(e){

        }
        var geocode = ymaps.geocode(document.city+', '+value);
        geocode.then(succes_getGeopointByAddress);
        return this;
    }

    function succes_getGeopointByAddress(res) {
        if (res.geoObjects.getLength()) {
            ps.geopoint = res.geoObjects.get(0).geometry.getCoordinates();
            drawMap();
        }
    }

    function parseAdressData(data) {
        var location = data.data('geopoint').split(';');
        ps.geopoint = [parseFloat(location[0].replace(',','.')), parseFloat(location[1].replace(',','.'))];
        ps.address = data[0].innerText
    }

    function initMap() {
        ps.map = new ymaps.Map("YMapsID", {
                center: ps.geopoint,
                zoom: 15,
                controls: ['zoomControl', 'fullscreenControl', 'geolocationControl']
            }
        );
        ps.map_is_init = true;
    }

    function drawMap() {
        if (!ps.map_is_init) {
            initMap();
        }
        if (ps.address_placemark)
            ps.map.geoObjects.remove(ps.address_placemark);
        ps.map.setCenter(ps.geopoint);
        ps.address_placemark = new ymaps.Placemark(ps.geopoint, { balloonContent: ps.address }, {
                iconLayout: 'default#image',
                iconImageHref: '/static/i/map/marker_sm.png',
                iconImageSize: [36, 35],
                iconOffset: [2, 0]
            });
        ps.map.geoObjects.add(ps.address_placemark);
        ps.address_placemark.balloon.open()
    }

    function set_new_address() {
        parseAdressData($(this).parent());
        if (ps.map_tab.is(':visible'))
            drawMap()
    }

    function handler_mapShow() {
        parseAdressData(ps.address_holder);
        if (!ps.geopoint[0] || !ps.geopoint[1]) {
            getGeopointByAddress();
        } else {
            drawMap();
        }
    }

    ps.init = function () {
        ps.address_holder = $('#address_holder');
        ps.address_switcher = $('#address_switcher');
        ps.address_switcher_text = $('#btntxt');
        ps.more_addresses = $('.dropdown__list');
        ps.map_is_init = false;
        ps.address_placemark = false;

        ps.map_tab = $('.pane.place__map');
        ps.map_tab.bind('show.tab', handler_mapShow);
        if (ps.map_tab.is(':visible')){
            handler_mapShow();
        }

        ps.more_addresses.droplist();

        ps.more_addresses.find('.dropdown__item span').each(function () {
            $(this).click(set_new_address);
        });
        return this;
    }

    ymaps.ready(function () {
        ps.init();
    });

    $('.place-photos').justifiedGallery({
        rowHeight: 160,
        sizeRangeSuffixes: {
            'lt100':'',
            'lt240':'', 
            'lt320':'', 
            'lt500':'', 
            'lt640':'', 
            'lt1024':''
        },
        captions: false,
        justifyLastRow: false
    });
})()