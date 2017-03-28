(function($) {

$.fn.rating = function (feedback_msg) {
    
  return this.each(function () {
    var form = this;

    function ajax_submit() {
      var button = $(this);
      var vote = button.val();
      var url = $(form).attr("action");
      var csrf = $("input[name=csrfmiddlewaretoken]", form).val();
      var data = {vote: vote,
                  is_ajax: true,
                  csrfmiddlewaretoken: csrf};

        $(".star-rating", form).remove().children().appendTo(form).end();
        $(".current-votes", form).fadeOut('slow', function() {
            // Animation complete.
            $("ol", form).append('<li class="rating-feedback">' + feedback_msg + '</li>');
            var feedback = $(".rating-feedback", form);
            feedback.fadeOut(4500);
        });

      $(form).load(url, data, function() {
        /*
          $(".star-rating", form).remove().children().appendTo(form).end();
          if (feedback_msg) {
          $("ol", form).append('<li class="rating-feedback">' + feedback_msg + '</li>');
          var feedback = $(".rating-feedback", form);
          feedback.fadeOut(4500);
        }
        $("input[type=submit]", form).click(ajax_submit);
         */
        });
      return false;
    };

    $("input[type=submit]", form).click(ajax_submit); 
  });

};

})(jQuery);
