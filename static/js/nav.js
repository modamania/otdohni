var MainMenu = {
    init: function() {
        this.menu = $('.menu'),
        this.itemsList = this.menu.find('.menu__layout');
        this.items = this.itemsList.find('.menu__item');
        this.specials = this.items.filter('.menu__item_special_yes');
        this.specials_width = this.specials.width();
        this.more = this.menu.find('.menu__more');
        this.more_width = this.more.width();
        this.moreDropdown = this.menu.find('.menu__dropdown');
        this.timeout = false;

        this.bindUI();
        this.setWidth();
        this.resize();
    },
    bindUI: function() {
        $(window)
            .on('resize', $.proxy(this.handler_window_resize, this))
            .on('click.morenav', '.menu__more', function(e){
                e.preventDefault();
                e.stopPropagation();
                MainMenu.toggleMore();
            })
            .on('click.morenav', '.menu__dropdown', function(e){
                e.stopPropagation();
            })
            .on('click.morenav', function(){
                MainMenu.hideMore();
            })
            .on('keyup', function(e){
                if (e.keyCode == 27) {
                    MainMenu.hideMore();
                }
            });
    },
    handler_window_resize: function () {
        clearTimeout(this.timeout);
        this.timeout = setTimeout(this.resize(), 100);
    },
    resize: function() {
        var max_width = this.menu.width() - this.more_width - this.specials_width,
            now_width = 0,
            hide_count = 0;
        $(this.items).not('.menu__item_special_yes').each(function () {
            var o = $(this);
            now_width += o.data('width');
            if (now_width > max_width) {
                o.hide();
                hide_count += 1;
            } else {
                o.show();
            }
        });

        if (hide_count) {
            $('.menu__item', this.moreDropdown).hide().slice(hide_count*-1).show();
        }

        this.menu.toggleClass('is-cropped', hide_count > 0);
    },
    setWidth: function(){
        $.each(this.items, function(){
            var self = $(this);
            self.data('width', self.width())
        });
    },
    toggleMore: function(){
        MainMenu.moreDropdown.toggleClass('is-visible');
    },
    hideMore: function(){
        MainMenu.moreDropdown.removeClass('is-visible');
    }
}

$(function(){
    MainMenu.init();    
});