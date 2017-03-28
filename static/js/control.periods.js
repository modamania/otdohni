$(function(){
    function selectNoRepeat(elem){
        if (!elem){
            var elem = $('input[id$=repeat_on_0]');
        } else {
            var elem = $(elem);
        }
        elem.parents('span.clearfix').next('.repeat_settings').hide();
    };

    function selectRepeatDay(elem){
        if (!elem){
            var elem = $('input[id$=repeat_on_1]');
        } else {
            var elem = $(elem);
        }
        var settings = elem.parents('span.clearfix').next('.repeat_settings');
        settings.show();
        settings.find('.weekday_checkbox').hide();
        settings.find('#interval').text('днях');
    };

    function selectRepeatWeek(elem){
        if (!elem){
            var elem = $('input[id$=repeat_on_2]');
        } else {
            var elem = $(elem);
        }
        var settings = elem.parents('span.clearfix').next('.repeat_settings');
        settings.show();
        settings.find('.weekday_checkbox').show();
        settings.find('#interval').text('неделях');
    };

    $('.repeat_on input[type=radio]:checked').each(function(){
        var id = $(this).attr('id');
        var repeat_on = id[id.length - 1];

        if (repeat_on == '0'){
            selectNoRepeat(this);
        }
        if (repeat_on == '1'){
            selectRepeatDay(this);
        }
        if (repeat_on == '2'){
            selectRepeatWeek(this);
        }
    });

    $('input[id$=repeat_on_0]').click(function(){
        selectNoRepeat(this)
    });

    $('input[id$=repeat_on_1]').click(function(){
        selectRepeatDay(this)
    });

    $('input[id$=repeat_on_2]').click(function(){
        selectRepeatWeek(this)
    });
});
