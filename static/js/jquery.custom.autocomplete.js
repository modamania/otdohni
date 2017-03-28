(function($) {
$.fn.myautocomplete = function (options) {
    var options = jQuery.extend({
        length_for_request : '0',
        delay_for_request : '1000',
        prefix_for_url_all_result: '',
        url_for_ajax : '',
        in_action : false,
        popup_is_init : false,
        popup_is_visible : false,
        popup : null,
        container : null,
        ignore_click : false,
        link_all_results : '',
        container_not_empty : false,
        searchword : '',
        input_object : null,
        popup_class : 'b-search-autocomplete',
        container_class : 'b-search-results',
        all_results_class : 'b-search-all-results',
        all_results_text : 'Все результаты',
        button_close_class : 'close',
        item_list : new Array(),
        selected_index : null,
        is_selected : false,


        popup_init : function () {
            if (options.popup_is_init == false){
                options.popup = jQuery('<div>').attr('class', options.popup_class).hide();
                var offset = options.input_object.offset();
                options.popup.css('top', (offset.top + get_height(options.input_object)) + 'px');
                options.popup.css('left', offset.left + 'px');
                options.popup.css('width', get_width(options.input_object) + 'px');
                options.container = jQuery('<div>').addClass(options.container_class);
                options.popup.append(options.container);
                options.link_all_results = jQuery('<a>').attr('href', '').text(options.all_results_text);
                jQuery('<div>').addClass(options.all_results_class).html(options.link_all_results).appendTo(options.popup);
                jQuery('<div>').addClass(options.button_close_class).click(options.popup_hide).appendTo(options.popup);
                options.popup.appendTo('body');
                options.popup.mousedown(function () {options.ignore_click = true}).mouseup(function () {options.ignore_click = false;});
                options.popup_is_init = true;
            } else {
                options.container.html('');
            }
        },

        popup_show : function () {
            if (options.popup_is_init){
                options.popup.show();
                options.popup_is_visible = true;
            }
        },

        popup_hide : function () {
            if (options.popup_is_init && options.ignore_click == false){
                options.popup.hide();
                options.popup_is_visible = false;
                options.is_selected = false;
            }
        },

        draw_result : function (data) {
            options.container_not_empty = false;
            options.popup_init();

            options.item_list = new Array();

            var limit_for_items = 10
            if (data.container_list.length == 2){
                limit_for_items = 5
            }
            if (data.container_list.length == 3){
                limit_for_items = 3
            }
            if (data.container_list.length == 4){
                limit_for_items = 3
            }
            jQuery.each(data.container_list, function (container_key, container_item) {

                options.container_not_empty = true;
                var div_item = jQuery('<div>').addClass('b-search-results-item');
                var counter = 0;
                if (container_item.item_list.length != 0){

                    jQuery('<div>').addClass('item-title').text(container_item.title).appendTo(div_item);

                    var ul = jQuery('<ul>');
                    jQuery.each(container_item.item_list, function (item_key, item) {
                        if (counter < limit_for_items){
                            counter++;
                            var li = jQuery('<li>');
                            li.append(jQuery('<a>').attr('href', item.url).text(item.title));
                            ul.append(li);
                            options.item_list.push(li);
                        }
                    });

                }
                div_item.append(ul);
                options.container.append(div_item);
            });
            options.container.find('div.b-search-results-item:last').addClass('b-search-results-item-last');
            if (options.container_not_empty == true) {
                options.link_all_results.attr('href', options.prefix_for_url_all_result + options.searchword).text(options.all_results_text + ' (' + data.item_length +')');
                options.popup_show();
            } else {
                options.popup_hide();
            }
        },

        select_next : function (to_down) {
            switch (to_down){
                case false:
                    if (options.selected_index == 0)
                        options.selected_index = (options.item_list.length - 1);
                    else
                        options.selected_index--;
                    break;
                case true:
                default:
                    if (options.selected_index == (options.item_list.length - 1))
                        options.selected_index = 0;
                    else
                        options.selected_index++;
            }
            options.item_list[options.selected_index].addClass('hover');
        },

        selected_down : function () {
            if (options.selected_index == null) {
                options.item_list[0].addClass('hover');
                options.selected_index = 0;
            } else {
                options.item_list[options.selected_index].removeClass('hover');
                options.select_next(true);
            }
        },

        selected_up : function () {
            if (options.selected_index == null) {
                options.item_list[(options.item_list.length - 1)].addClass('hover');
                options.selected_index = (options.item_list.length - 1);
            } else {
                options.item_list[options.selected_index].removeClass('hover');
                options.select_next(false);
            }

        },

        select_next_handler : function (to_down) {
            if (options.popup_is_visible){
                options.is_selected = true;
                switch (to_down){
                    case false:
                        options.selected_up();
                        break;
                    case true:
                    default:
                        options.selected_down();
                        break;
                }
            }
        },

        selected_go : function () {
            if (options.is_selected){
                if (options.selected_index != null)
                    document.location.href = (options.item_list[options.selected_index].find('a:first').attr('href'));
                return true;
            }
        }

    }, options);


    var get = function (obj) {
        options.in_action = true;
        var val = obj.val();
        jQuery().delay(options.delay_for_request);
        if (obj.val() != val){
            options.in_action = false;
        } else {
            options.searchword = obj.val();
            jQuery.getJSON(options.url_for_ajax, {'t': options.searchword, 'a': '1'},
                options.draw_result
            );
            options.in_action = false;
        }
    }

    var get_width = function (obj) {
        return obj.innerWidth();
    }
    var get_height = function (obj) {
		return obj.outerHeight();
    }

    return this.each(function () {

        options.input_object = $(this);
       jQuery(options.input_object).keyup(function (e) {
            switch (e.keyCode){

                //стрелка вверх
                case 38:
                    options.select_next_handler(false);
                    break;

                //стрелка вниз
                case 40:
                    options.select_next_handler(true);
                    break;
                //Enter
                case 13:
                    if (options.selected_go())
                        return false;
                    break;

                case 27:
                    options.popup_hide();
                    break;

                default:
                    if ($(this).val().length > options.length_for_request){
                        if (options.in_action == false){
                            get($(this));
                        }
                    } else {
                        options.popup_hide();
                    }
            }
        }).focusout(options.popup_hide);
        jQuery(document).click(options.popup_hide);
    });

};
})(jQuery);
