{# load tagging_tags #}

$(function() {
    {# tags_for_model photoreport.PhotoReport as report_tags #}

    var data = "{{ report_tags|join:',' }}".split(",");
    $("#id_tags").autocomplete(data, {
        'width': 150,
        'max': 10, 
        'multiple': true,
        'multipleSeparator': ", ",
        'scroll': true,
        'scrollHeight': 300,
        'matchContains': true,
        'autoFill': true,
    });
})

