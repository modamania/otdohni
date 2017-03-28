(function($) {
    var defaults = {
        container: false,
        close_button: false,
        toggleShow: false,
        on_show: function(){},
        on_hide: function(){},
        hide_by_click: function (e) {
            var self = this;
            self.deactivate();
            return self;
        },
        hide_by_keypress: function (e) {
            var self = this;

            if (e.keyCode == "27") {
                self.deactivate();
            }
            return self;
        },
        activate: function() {
            var self = this;
            
            self.toggleClass('is-visible', !self.is('.is-visible'));

            $(document)
                .on('click.popup', function (e) {
                    self.hide_by_click(e);
                })
                .on('keyup.popup', function (e) {
                    self.hide_by_keypress(e);
                });

            self.on_show();

            return false;
        },
        deactivate: function() {
            var self = this;

            self.removeClass('is-visible');

            $(document)
                .off('.popup');

            self.on_hide();
        },
        click: function (e) {
            var container = $(this).data('container');
            e.preventDefault();
            e.stopPropagation();
            if (container.is('.is-visible')){
                container.deactivate();
            } else {
                container.activate();
            }
            return false;
        }
    };


    var methods = {
        init : function(params) {
            return $(this).each(function () {
                var options = $.extend({}, defaults, params),
                    container = $(options.container),
                    $this = $(this);

                container.activate = options.activate;
                container.deactivate = options.deactivate;
                container.on_show = options.on_show;
                container.on_hide = options.on_hide;
                container.hide_by_click = options.hide_by_click;
                container.hide_by_keypress = options.hide_by_keypress;

                if (options.close_button){
                    close_button = $(options.close_button);
                    close_button.on('click.popup', function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        container.deactivate();
                    });
                }

                container.on('click', function(e){
                    e.stopPropagation();
                });

                $this.data('container', container);

               return $this.on('click.popup', options.click);
            });
        },
        show: function () {
            self = this.data('container');
            self.activate();
        },
        hide: function () {
            self = this.data('container');
            self.deactivate();
        }
    };


    $.fn.popup = function(method){
        // немного магии
        if ( methods[method] ) {
            // если запрашиваемый метод существует, мы его вызываем
            // все параметры, кроме имени метода прийдут в метод
            // this так же перекочует в метод
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            // если первым параметром идет объект, либо совсем пусто
            // выполняем метод init
            return methods.init.apply( this, arguments );
        } else {
            // если ничего не получилось
            $.error( 'Method "' +  method + '" not fined in jQuery.popup' );
        }
    };
})(jQuery);
