$(function() {
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
    }

    $(window)
    .on('scroll', function(){    
        getscroll();
            
        var msgs = $('.messages'),
            panel = $('.messages__toolbar'),
            width = msgs.width(),
            top = msgs.offset().top;
            
            panel.toggleClass('messages__toolbar_fixed', yScroll > top)
            
            resizeToolbar();
    })
    .on('resize', function(){
        resizeToolbar();
    });

    function resizeToolbar(){
       var msgs = $('.messages'),
           panel = $('.messages__toolbar');

        panel.css('width', msgs.width());
    }

    function ToolbarFilter(el, messages_list) {
        var self = $(el);
        var all = $('li[data-selector=all]', self);
        var read = $('li[data-selector=read]', self);
        var unread = $('li[data-selector=unread]', self);
        var none = $('li[data-selector=none]', self);

        all.click(function () {
            messages_list.message('checked', true);
            self.addClass('hidden');
        });

        read.click(function () {
            messages_list.message('checked', 'read');
            self.addClass('hidden');
        });

        unread.click(function () {
            messages_list.message('checked', 'unread');
            self.addClass('hidden');
        });

        none.click(function () {
            messages_list.message('checked', false);
            self.addClass('hidden');
        });

        return self;
    }

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

    function set_disable(el) {
        el.addClass('btn_state_disabled')
            .find('input')
            .prop('disabled', true);
    }

    function set_enable(el) {
        el.removeClass('btn_state_disabled')
            .find('input')
            .prop('disabled', false);
    }

    $.fn.message = function( method ) {
        var methods = {
            init: function () {
                var self = $(this);
                var init = self.data('message');
                if (init){
                } else {
                    var m = new Message(this);
                    self.data('message', m);
                }
                return this;
            },
            checked: function (is_checked) {
                this.each(function () {
                    var m = $(this).data('message');
                    m.checked(is_checked);
                });
                return this;
            },
            get_checked: function (type) {
                var arr = [];
                this.each(function () {
                    var m = $(this).data('message');
                    switch (type) {
                        case undefined:
                            if (m.is_checked())
                                arr.push(this);
                            break
                        case 'unread':
                            if (m.is_checked() && m.unread())
                                arr.push(this);
                            break
                        case 'read':
                            if (m.is_checked() && m.unread() == false)
                                arr.push(this);
                            break
                        default:
                            break
                    }
                });
                return $(arr);
            },
            get_id: function () {
                var m = $(this).data('message');
                return m.get_id();
            }
        }

        if ( methods[method] ) {
            var arg = Array.prototype.slice.call( arguments, 1 );
            return methods[ method ].apply( this, arg);
        } else if ( typeof method === 'object' || ! method ) {
            var arg = arguments;
            return this.each(function () {methods.init.apply( this, arg );});
        } else {
            $.error( 'Method "' +  method + '" not found in jQuery.message.' );
        }
    }

    var messages_list = $('#messages_list').find('.messages__item');
    messages_list.message();

    var tools = {}
    tools.lock_toggle_switcher = false;
    tools.self = $('#messages__toolbar');

    tools.checkbox = $('input[type=checkbox]', tools.self);
    tools.checkbox.click(function() {
        all = $('li[data-selector=all]');
        none = $('li[data-selector=none]');
        
        if (Boolean($('.messages__item [checked="checked"]').length)) {
            none.click();
        } else {
            all.click()
        }
        tools.lock_toggle_switcher = true;
    });

    tools.filter = new ToolbarFilter($('.messages__filter', tools.self), messages_list);

    tools.statusbar = $('.messages__status', tools.self);

    tools.change_selected = function () {
        var count = messages_list.message('get_checked').length;
        var is_selected = Boolean(count);
        tools.checkbox.attr('checked', is_selected);
        if (is_selected){
            tools.statusbar.text('Выбрано ' + count + GetNoun(count, ' сообщение', ' сообщения', ' сообщений'));
            set_enable(tools.btn_remove);
            var count_unread = messages_list.message('get_checked', 'unread').length;
            if (count_unread) {
                set_enable(tools.btn_mark_reader);
                tools.btn_mark_reader.show();
                tools.btn_mark_unreader.hide();
            } else {
                tools.btn_mark_reader.hide();
                set_enable(tools.btn_mark_unreader);
                tools.btn_mark_unreader.show();
            }
        } else {
            tools.statusbar.text('');
            set_disable(tools.btn_remove);
            set_disable(tools.btn_mark_reader);
            tools.btn_mark_reader.show();
            tools.btn_mark_unreader.hide();
            set_disable(tools.btn_mark_unreader);
        }
    }

    tools.switcher = $('.messages__selector', tools.self);
    tools.switcher.click(function () {
        tools.filter.toggleClass('hidden');
    });

    tools.btn_mark_reader = $('.btn_mark_reader', tools.self);
    tools.btn_mark_unreader = $('.btn_mark_unreader', tools.self);
    tools.btn_remove = $('.btn_remove', tools.self);
    tools.btn_remove.click(remove_checked_message);
    tools.btn_mark_reader.click(mark_as_read);
    tools.btn_mark_unreader.click(mark_as_unread);

    function remove_checked_message() {
        if (tools.btn_remove.hasClass('btn_state_disabled') == false){
            var list = messages_list.message('get_checked')
            var m_id = []
            list.each(function () {
                m_id.push($(this).message('get_id'));
            });
            var params = {}
            params.m_id = m_id;
            params.next = window.location.pathname;
            params = $.param(params, true);
            window.location.href = '/messages/delete_list/?'+params;
        }
    }

    function mark_as_read() {
        if (tools.btn_mark_reader.hasClass('btn_state_disabled') == false){
            var list = messages_list.message('get_checked', 'unread')
            var m_id = []
            list.each(function () {
                m_id.push($(this).message('get_id'));
            });
            var params = {}
            params.m_id = m_id;
            params.next = window.location.pathname;
            params = $.param(params, true);
            window.location.href = '/messages/mark_as_read/?'+params;
        }
    }

    function mark_as_unread() {
        if (tools.btn_mark_unreader.hasClass('btn_state_disabled') == false){
            var list = messages_list.message('get_checked', 'read')
            var m_id = []
            list.each(function () {
                m_id.push($(this).message('get_id'));
            });
            var params = {}
            params.m_id = m_id;
            params.next = window.location.pathname;
            params = $.param(params, true);
            window.location.href = '/messages/mark_as_unread/?'+params;
        }
    }

    function Message(el) {
        var self
        var id
        var is_checked
        var checkbox
        var unread

        this.init = init;
        this.checked = checked;
        if (typeof el != undefined)
            init(el);
        this.is_checked = function () {
            return is_checked
        }
        this.unread = function () {
            return unread
        }
        this.get_id = function () {
            return id
        }

        function init(el) {
            self = $(el);
            id = self.attr('data-id');
            checkbox = $('input[type=checkbox]', self);
            unread = self.hasClass('messages__item_state_unread');
            checkbox.change(function () {
                checked(!is_checked);
            });
        }

        function checked(new_checked) {
            if (typeof new_checked == 'boolean'){
                is_checked = new_checked;
            } else if (typeof new_checked == 'string') {
                is_checked = false;
                switch (new_checked) {
                    case 'read':
                        if (!unread)
                            is_checked = true;
                        break
                    case 'unread':
                        if (unread)
                            is_checked = true;
                        break
                    default:
                        break
                }
            }
            checkbox
                .attr('checked', is_checked)
                .closest('.messages__item').toggleClass('messages__item_state_selected', checkbox.prop('checked'));
            tools.change_selected();
        }
    }
})
