$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

django.jQuery(document).ready(function() {
    django.jQuery('.form-row.photoreports').before('<div id="attributes_photo"></div>');
    django.jQuery('.form-row.actions').before('<div id="attributes_action"></div>');
    django.jQuery('.form-row.events').before('<div id="attributes_event"></div>');
    django.jQuery('.form-row.newsitems').before('<div id="attributes_news"></div>');

    //PHOTO
    django.jQuery("#attributes_photo").html('<label style="margin-left: 10px;">Фильтр для фоторепортажей</label>' +
        '<p><label for="from_photo" style="float:none;">From</label></p>' +
        '<p><input type="text" id="from_photo" name="from" value="'+ DATE_FROM +'" /></p>' +
        '<p><label for="to_photo" style="float:none;">To</label></p>' +
        '<p><input type="text" id="to_photo" name="to" value="'+ DATE_TO +'"/></p>' +
        '<p><input type="button" value="Выбрать" id="submit_photo"/></p>')

    //ACTION
    django.jQuery("#attributes_action").html('<label style="margin-left: 10px;">Фильтр для акций</label>' +
         '<p><label for="from_action" style="float:none;">From</label></p>' +
         '<p><input type="text" id="from_action" name="from" value="'+ DATE_FROM +'" /></p>' +
         '<p><label for="to_action" style="float:none;">To</label></p>' +
         '<p><input type="text" id="to_action" name="to" value="'+ DATE_TO +'"/></p>' +
         '<p><input type="button" value="Выбрать" id="submit_action"/></p>')

    //EVENT
    django.jQuery("#attributes_event").html('<label style="margin-left: 10px;">Фильтр для событий</label>' +
        '<p><label for="from_event" style="float:none;">From</label></p>' +
        '<p><input type="text" id="from_event" name="from" value="'+ DATE_FROM +'" /></p>' +
        '<p><label for="to_event" style="float:none;">To</label></p>' +
        '<p><input type="text" id="to_event" name="to" value="'+ DATE_TO +'"/></p>' +
        '<p><select name="select_event_category" id="select_event_category"></select></p>' +
        '<input type="hidden" id="id_flag" value="0"/>' +
        '<p><input type="button" value="Выбрать" id="submit_event"/></p>')

    //NEWS
    django.jQuery("#attributes_news").html('<label style="margin-left: 10px;">Фильтр для новостей</label>' +
       '<p><label for="from_news" style="float:none;">From</label></p>' +
       '<p><input type="text" id="from_news" name="from" value="'+ DATE_FROM +'" /></p>' +
       '<p><label for="to_news" style="float:none;">To</label></p>' +
       '<p><input type="text" id="to_news" name="to" value="'+ DATE_TO +'"/></p>' +
       '<p><input type="button" value="Выбрать" id="submit_news"/></p>')

    //PHOTO_datepicker
	django.jQuery(function() {
		var dates = $( "#from_photo, #to_photo" ).datepicker({
			defaultDate: "+1w",
			changeMonth: true,
			numberOfMonths: 1,
            dateFormat:'dd-mm-yy',
			onSelect: function( selectedDate ) {
				var option = this.id == "from_photo" ? "minDate" : "maxDate",
					instance = $( this ).data( "datepicker" ),
					date = $.datepicker.parseDate(
						instance.settings.dateFormat ||
						$.datepicker._defaults.dateFormat,
						selectedDate, instance.settings );
				dates.not( this ).datepicker( "option", option, date );
			}
		});
	});

    //ACTION_datepicker
    django.jQuery(function() {
        var dates = $( "#from_action, #to_action" ).datepicker({
             defaultDate: "+1w",
             changeMonth: true,
             numberOfMonths: 1,
             dateFormat:'dd-mm-yy',
             onSelect: function( selectedDate ) {
                 var option = this.id == "from_action" ? "minDate" : "maxDate",
                     instance = $( this ).data( "datepicker" ),
                     date = $.datepicker.parseDate(
                         instance.settings.dateFormat ||
                             $.datepicker._defaults.dateFormat,
                         selectedDate, instance.settings );
                 dates.not( this ).datepicker( "option", option, date );
             }
         });
    });

    //EVENT_datepicker
    django.jQuery(function() {
        var dates = $( "#from_event, #to_event" ).datepicker({
           defaultDate: "+1w",
           changeMonth: true,
           numberOfMonths: 1,
           dateFormat:'dd-mm-yy',
           onSelect: function( selectedDate ) {
               var option = this.id == "from_event" ? "minDate" : "maxDate",
                   instance = $( this ).data( "datepicker" ),
                   date = $.datepicker.parseDate(
                       instance.settings.dateFormat ||
                           $.datepicker._defaults.dateFormat,
                       selectedDate, instance.settings );
               dates.not( this ).datepicker( "option", option, date );
           }
       });
    });

    //NEWS_datepicker
    django.jQuery(function() {
        var dates = $( "#from_news, #to_news" ).datepicker({
             defaultDate: "+1w",
             changeMonth: true,
             numberOfMonths: 1,
             dateFormat:'dd-mm-yy',
             onSelect: function( selectedDate ) {
                 var option = this.id == "from_news" ? "minDate" : "maxDate",
                     instance = $( this ).data( "datepicker" ),
                     date = $.datepicker.parseDate(
                         instance.settings.dateFormat ||
                             $.datepicker._defaults.dateFormat,
                         selectedDate, instance.settings );
                 dates.not( this ).datepicker( "option", option, date );
             }
         });
    });
    
    //PHOTOREPORTS
    django.jQuery('#submit_photo').click(function(){
        $.post(URL_FOR_FILTER, {
            id:OBJECT_ID,
            app:PHOTO_APP,
            model:PHOTO_MODEL,
            from:$('#from_photo').val(),
            to:$('#to_photo').val()
        },
        function(data){
            $("#id_photoreports_from").html(data['for_period']);
            $("#id_photoreports_to").html(data['chosen']);
            $("#id_photoreports").html(data['for_period']);
            $("#id_photoreports").append(data['chosen']);
            SelectBox.init('id_photoreports_from');
            SelectBox.init('id_photoreports_to');
        },
        "json");
        return false;
    });

    //NEWS
    django.jQuery('#submit_news').click(function(){
        $.post(URL_FOR_FILTER, {
                   id:OBJECT_ID,
                   app:NEWS_APP,
                   model:NEWS_MODEL,
                   from:$('#from_news').val(),
                   to:$('#to_news').val()
               },
               function(data){
                   if(data['succeed']){
                       $("#id_newsitems_from").html(data['for_period']);
                       $("#id_newsitems_to").html(data['chosen']);
                       $("#id_newsitems").html(data['for_period']);
                       $("#id_newsitems").append(data['chosen']);
                       $("#id_newsitems").show();

                       SelectBox.init('id_newsitems_from');
                       SelectBox.init('id_newsitems_to');
                   }
                   else{
                       alert("Smth goes wrong!");
                   }
               },
               "json");
        return false;
    });

    //ACTION
    django.jQuery('#submit_action').click(function(){
        $.post(URL_FOR_FILTER, {
                   id:OBJECT_ID,
                   app:ACTION_APP,
                   model:ACTION_MODEL,
                   from:$('#from_action').val(),
                   to:$('#to_action').val()
               },
               function(data){
                   $("#id_actions_from").html(data['for_period']);
                   $("#id_actions_to").html(data['chosen']);
                   $("#id_actions").html(data['for_period']);
                   $("#id_actions").append(data['chosen']);
                   SelectBox.init('id_actions_from');
                   SelectBox.init('id_actions_to');
               },
               "json");
        return false;
    });

    //EVENT
    django.jQuery('#submit_event').click(function(){
        var chosen=new Array();
        var i = 0;
        $('#id_events_to option').each(

            function(){
                chosen[i]=($(this).val());
                i=i+1;
            }
        );
        $.post(URL_FOR_FILTER_EVENTS, {
                   id:OBJECT_ID,
                   from:$('#from_event').val(),
                   to:$('#to_event').val(),
                   category_id:$('#select_event_category').val(),
                   chosen_list: chosen
               },
               function(data){
                   $('#select_event_category').html(data['categories']);
                   $('#select_event_category').append(data['current_category']);
                   $("#id_events_from").html(data['for_period']);
                   $("#id_events").html(data['for_period']);

                   if ($("#id_flag").val()=='0'){
                       $("#id_events_to").html(data['chosen']);
                       $("#id_events").append(data['chosen']);
                       $("#id_flag").val(1);
                   }


                   SelectBox.init('id_events_from');
                   SelectBox.init('id_events_to');

               },
               "json");
        return false;
    });

    // loading data to the select boxes
    django.jQuery('#submit_photo').click();
    django.jQuery('#submit_action').click();
    django.jQuery('#submit_news').click();
    django.jQuery('#submit_event').click();
});
