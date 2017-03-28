$(function(){
    $('.place_title #id_category, #id_tagging, #id_tags').multiselect();

    $('.promo_toggle').each(function () {
        var status_on = $(this).find('.promo_toggle__on');
        var status_off = $(this).find('.promo_toggle__off');
        var period = $(this).find('.promo_period');
        var input_promo = $(this).find('.promo__input input');
        status_on.click(function () {
            status_on.hide();
            status_off.show();
            input_promo.attr('checked', false);
        });
        status_off.click(function () {
            status_off.hide();
            status_on.show();
            input_promo.attr('checked', true);
        });
      });
});

// confirm place address delete
    $(function(){
        $(".address__delete").click(function(){
            if (window.confirm("Вы действительно хотите удалить адрес?")){
                $(this).nextAll("[name$=DELETE]").attr('checked', true);
                $(this).parents('.address_list__item').hide(500);

                return false;
            }
        })
    });