jQuery.fn.multiselect = function (options) {
     var options = jQuery.extend({
        pClass: 'parentselect',
        mClass: 'multiselect'
     }, options);

    return this.each(function () {
        thsObj = $(this);
        thsObj.hide();
        var pObj = jQuery('<div></div>').addClass(options.pClass);
        pObj.addClass(thsObj.attr('id'));
        pObj.insertAfter(this);
        var multiCloud = jQuery('<div></div>').addClass(options.mClass).appendTo(pObj);
        var mUl = jQuery('<ul></ul>');

        var option_list = jQuery(this).find('option');
        option_list.sort(function (a, b){
            var compA = $(a).text().toUpperCase();
            var compB = $(b).text().toUpperCase();
            return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
        })
        $.each(option_list, function () {
            var multiselect_item = jQuery(this);
              var item = jQuery('<li></li>').attr('rel', jQuery(this).val()).addClass('multiselect__selector');
              span = jQuery('<span class="pseudo">').text(jQuery(this).text());
              item.append(span)
               .bind('click', function () {
                  if (multiselect_item.attr('selected')){
                    multiselect_item.removeAttr('selected');
                    item.removeClass('selected');
                  } else {
                    multiselect_item.attr('selected', 'selected');
                    item.addClass('selected');
                  }
                  multiselect_item.change();
              })
               .hover(function () {jQuery(this).addClass('hover')}, function () {jQuery(this).removeClass('hover')});
            if (jQuery(this).attr('selected')) item.addClass('selected');
            mUl.append(item);
        });
        multiCloud.append(mUl);
    });
};
