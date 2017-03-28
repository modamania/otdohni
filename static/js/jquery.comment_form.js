(function($) {

    var init = function () {
        var self = $(this);
        var open_button = self.find('.open_form:first');
        var form = self.find('.form:first');
        var text = form.find('textarea:first');
        var close_button = self.find('.close_form:first');

        open_button.click(function(){
            $(this).hide();
            form.show();
            text.focus();
        });
        close_button.click(function(){
            open_button.show();
            form.hide();
        });

    }

    $.fn.comment_form = function() {
        return $(this).each(init);
    }
})(jQuery);
