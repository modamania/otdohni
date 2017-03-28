var first = true;
$(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'))
        }
    })
    var select_event = $('#id_event option:selected').val();
    var select_place = $('#id_place option:selected').val();

    function makeJson() {
        var date_val = $('input[name=date_event]').val()
        var date_list = date_val.split('.').map(function(x) {
            return parseInt(x)
        })
        return  {
            day: date_list[0],
            month: date_list[1],
            year: date_list[2],
        }
    }
    function setJson(data) {
        var data = eval(data)
        var event_select = $('#id_event')
        event_select.find('option').slice(1).remove();
        for (var i = 0; i < data.length; i++) {
            var item = data[i]
            var elem = $('<option>').val(item['id']).text(item['title'])
            event_select.append(elem);
        }
        if (first) {
            $('#id_event option[value=' + select_event + ']').attr('selected', true);
            $('#id_place option[value=' + select_place + ']').attr('selected', true);
            first = false;
        }
    }
    var button = $("<input type='button' value='Выбрать' id='submit_date'>")
    button.click(function() {
        var date_json = makeJson()
        $.post(API_URL_EVENT_ON_DAY, date_json, setJson);
    })
    $('.form-row.date_event').append(
            $('<div>').attr('id', 'attributes_event'));
    $('#attributes_event').append(button);

    $('#id_event').live('change', function() {
        var val = $(this).find(':selected').val()
        if (val) {
            $.post(API_URL_PLACE_FOR_EVENT, {
                'event_id': val,
            }, function(data) {
                var data = eval(data);
                var place_select = $('#id_place')
                place_select.find('option').slice(1).remove();
                for (var i = 0; i < data.length; i++) {
                    var item = data[i]
                    var elem = $('<option>').val(item['id']).text(item['title'])
                    place_select.append(elem);
                };
            })
        }
    });
    button.click();

})
