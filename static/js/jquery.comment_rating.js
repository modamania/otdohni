(function($) {

    var prefixClass = 'comment__rating__';

    var get_count = function(button) {
        var count = button.data('count');
        if (count){
        } else {
            var count = button.next('span');
        }
        return count;
    }

    var get_count_var = function(count) {
        return count_var = parseInt(count.text());
    }

    var down_count = function(button) {
        var count = get_count(button);
        var count_var = get_count_var(count);
        count_var = count_var - 1;
        if (count_var < 0)
            count_var = 0;
        count.text(count_var);
    }

    var up_count = function(button) {
        var count = get_count(button);
        var count_var = get_count_var(count);
        count_var = count_var + 1;
        count.text(count_var);
    }

    var select_button = function(button) {
        var button_type = button.data('relate');
        button.removeClass(prefixClass + button_type);
        button.addClass(prefixClass + 'current');
    }

    var deselect_button = function(button) {
        var button_type = button.data('relate');
        button.removeClass(prefixClass + 'current');
        button.addClass(prefixClass + button_type);
    }

    var button_click = function() {
        var button = $(this);
        var id = button.data('id');
        var button_type = button.data('relate');

        if (button.hasClass('comment__rating__current')) {
            var relate = 'current';
            var action = 'remove_vote';
        } else {
            var relate = button_type;
            var action = relate;
        }
        var url = '/api/comment/relate/' + [action, id].join('/') + '/';
        $.ajax({
            url: url,
            success: function (){
                if (relate == 'current'){
                    deselect_button(button);
                    down_count(button);
                } else {
                    button.addClass(prefixClass + 'current');
                    var opposite_button = button.data('opposite_button');
                    up_count(button);
                    down_count(opposite_button);
                    deselect_button(opposite_button);
                    select_button(button);
                }
            }
        });
    }

    var init = function() {
        var self = $(this);
        var id = self.data('id');
        agree = self.find('span[data-relate=agree]');
        disagree = self.find('span[data-relate=disagree]');
        //self.find('span.pseudo').data('id', id).click(button_click);
        agree.data('id', id).data('opposite_button', disagree).click(button_click);
        disagree.data('id', id).data('opposite_button', agree).click(button_click);
    }

    $.fn.comment_rating = function() {
        return $(this).each(init);
    }
})(jQuery);
