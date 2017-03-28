function fotoreportAdd() {
	$('#fotorepot_data .reports-list').append('<div class="item"><dl><dt>Заголовок</dt><dd><input name="title[]" type="text" value=""></dd></dl><dl><dt>Описание</dt><dd><input name="about[]" type="text" value=""></dd></dl><dl><dt>Ссылка</dt><dd><input name="link[]" type="text" value=""></dd></dl><span class="close"><img onclick="$(this).parent().parent().remove();" src="templates/oo/i/close.gif"></span></div>');
}
function fotoreportSubmit() {
	var no_error = 1;
	preg_link = /http:\/\/(?:www\.)?otdohniomsk.ru\/(?:.*)?/i;
	$('#fotorepot_data div').each( function() {
		$(this).find(':input').each(function () {
			switch ($(this).attr('name')){
				case 'link[]':
					if (!preg_link.test($(this).attr('value'))) {$(this).css('background', 'red'); no_error = 0}
					else $(this).css('background', '');
					break;
				case 'title[]':
					if ($(this).attr('value') == undefined) {$(this).css('background', 'red'); no_error = 0}
					else $(this).css('background', '');
					break;
				case 'about[]':
					if ($(this).attr('value') == undefined) {$(this).css('background', 'red'); no_error = 0}
					else $(this).css('background', '');
					break;
			}
		});
	});
	if (no_error) $(this).send();
}