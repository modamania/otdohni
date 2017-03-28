$(function(){

	$('.tabs-box').on('click', '.tab', function(e){
		$this = $(this);
	        $this
	        	.addClass('tab_state_current')
	        	.siblings()
	        	.removeClass('tab_state_current');
	        $(e.delegateTarget)
	        	.find('.pane')
	        	.removeClass('pane_state_current')
	        	.eq($this.index()).addClass('pane_state_current');
	});

	$('.accordion').on('show', function () {
	  console.log($(this))
	});

	$('.search_pos_top')
		.on('click', '.search__submit', function(e){
			var form = $(e.delegateTarget);

			console.log(form)

			if (!form.data('visible')){
				e.preventDefault();
				form
					.data('visible','yes')
					.addClass('search_visible_yes');
			}

		})
		.on('click','.search__close', function(e){
			var form = $(e.delegateTarget);

			form
				.data('visible','')
				.removeClass('search_visible_yes');
		});
});

