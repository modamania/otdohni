$.fn.scrollfoto = function (options) {
     var options = $.extend({
     thsImgClss: 'active',
     scrFst: '108',
     innerDivClass: 'scrllft',
     wrapDivClass: 'wrpft',
     arrowUpClass: 'arrwupft',
     arrowDownClass: 'arrwdwnft',
     offsetUp: '5',
     offsetDown: '5'
     }, options);

  return this.each(function () {
    var thsObj = $(this),
        limit = 0,
        arrowUp,
        arrowDown,
        ulTop;

    thsObj
      .wrap($('<div class="' + options.wrapDivClass + '" />'));

    var thsWrap = thsObj.parent();

    thsObj.wrap($('<div class="' + options.innerDivClass + '" />'));

    var thsImage = thsObj.find('.'+options.thsImgClss),
        thsIndex = thsImage.data('pos'),
        start = thsIndex - options.offsetUp;

    start = start < 0 ? 0 : start;

    var stop = thsIndex + options.offsetDown,
        thumbs = thsObj.find('li'),
        thumbsTotal = thumbs.length,
        heightImg = thsImage.outerHeight(true);

    thsObj
      .find('li a')
      .slice(start, stop--)
      .each(function () {
        DrawImage(this)
      });

    thumbs.last().addClass('last');

    ulBottom = thumbsTotal * heightImg - thsObj.parent().height();

    ulTop = thsIndex * heightImg * -1 + heightImg * 2;

    arrowUp = $('<div class="' + options.arrowUpClass + '">')
                .append(
                  $('<span />')
                    .hover(function(){
                      $(this).toggleClass('hover')
                    })
                  .append('<i />'))
                .on('mousedown', function () {
                  scrollUp(heightImg)
                })
                .prependTo(thsWrap);

    arrowDown = $('<div class="' + options.arrowDownClass + '" />')
                  .append(
                    $('<span />')
                      .hover(
                        function(){
                          $(this).toggleClass('hover')
                        })
                        .append('<i />'))
                      .on('mousedown', function () {
                        scrollDown(heightImg)
                      })
                      .appendTo(thsWrap);

    if (ulTop >= 0){
      ulTop = 0;
      arrowUp.addClass('disabled');
    }

    if (Math.abs(ulTop) >= ulBottom){
      ulTop = ulBottom * -1;
      arrowDown.addClass('disabled');
    }

    thsObj.css('top', ulTop+'px');

    var newUlTop = ulTop;

    thsObj.mousewheel(function (event, delta) {
      if (delta > 0) {
        scrollUp(options.scrFst);
      } else if (delta < 0) {
        scrollDown(options.scrFst);
      }
      event.stopPropagation();
      event.preventDefault();
    });

    function scrollUp(pitch){
      newUlTop = ulTop + pitch * 1 + 1;

      if (newUlTop >= 0){
        newUlTop = 0;
        arrowUp.addClass('disabled');
      }

      if (start > 0) {
        start--;
        add_img(start);
      }

      arrowDown.removeClass('disabled');
      AnimateonScroll(newUlTop);
    }

    function scrollDown(pitch){
      newUlTop = ulTop - pitch + 1;
      if (Math.abs(newUlTop) >= ulBottom){  
        newUlTop = ulBottom * - 1;
        arrowDown.addClass('disabled');
      }
      arrowUp.removeClass('disabled');
      if (stop < thumbsTotal) {
        stop++;
        add_img(stop);
      }
      AnimateonScroll(newUlTop);
    }
    function AnimateonScroll(newTop) {
      if (newTop != ulTop) {
       thsObj.stop();
       thsObj.animate({'top': newTop}, options.scrDlay);
       ulTop = newTop;
      }
    }
    function DrawImage(t) {
      $('<img />').attr('src', $(t).attr('rel')).appendTo(t);
    }
    function add_img(indexAddImg) {
      thsObj.find('li a').eq(indexAddImg).each(function () {DrawImage(this)});
    }
  });
};
