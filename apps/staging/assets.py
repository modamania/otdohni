from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle('js/calendar.js',
               'js/nav.js',
               'js/main.js',
              ),
        filters='jsmin',
        output='cache/packed.js')


register('admin_js',
        Bundle('js/jquery.multiselect.js',
               'js/cpanel.js',
              ),
        filters='jsmin',
        output='cache/packed.admin.js')


register('control_js',
        Bundle('js/jquery.formset.min.js',
               'js/jquery.autocomplete.js',
               'js/jquery.ui.selectable.js',
               'js/jquery-ui-i18n.js',
               'js/jquery.Jcrop.js',
               'js/jquery.upload.js',
               'js/control.js',
               'elrte/js/elrte.min.js',
               'elrte/js/i18n/elrte.ru.js',
               'elfinder/js/elfinder.min.js',
               'elfinder/js/i18n/elfinder.ru.js',
               'js/jquery.ui.widget.js',
               'js/tmpl.min.js',
               'js/load-image.min.js',
               'js/canvas-to-blob.min.js',
               'js/bootstrap.min.js',
               'js/bootstrap-image-gallery.min.js',
               'js/jquery.iframe-transport.js',
               'js/jquery.fileupload.js',
               'js/jquery.fileupload-fp.js',
               'js/jquery.fileupload-ui.js',
               'js/locale.js',
               'js/upload.js',
              ),
        filters='jsmin',
        output='cache/packed.control.js')

register('libs_js',
        Bundle('js/jquery.custom.autocomplete.js',
               'js/jquery.popup.js',
               'js/jquery.infieldlabel.min.js',
               'js/jquery.fancybox.pack.js',
               'js/jquery.comment_form.js',
               'js/jquery.comment_rating.js',
               'js/jquery.scrollfoto.js',
               'js/jquery.rating.js',
               'js/jquery.easing-1.3.pack.js',
               'zforms/js/ZForms-jquery-3.0.4-min.js',
               'js/jquery.bxslider.min.js',
               'js/jquery.reveal.js',
               'js/tmpl.min.js'
              ),
        filters='jsmin',
        output='cache/packed.libs.js')

register('js_ui',
        Bundle('js/jquery-ui-1.8.13.custom.min.js',
               'js/jquery.ui.autocomplete.js',
               'js/jquery.ui.dialog.js',
               'js/jquery.ui.tabs.js',
               'js/jquery.ui.selectable.js',
               'js/jquery.ui.draggable.js',
               'js/jquery.ui.droppable.js',
               'js/jquery.ui.resizable.js',
              ),
        filters='jsmin',
        output='cache/packed.ui.js')

#CSS
register('all_css',
        Bundle('css/bootstrap.min.css',
               'css/bootstrap-image-gallery.min.css',
               'css/reveal.css',
               'zforms/css/ZForms-screen.css',
               'css/jquery.fancybox.css',
               'css/jquery-ui-1.8.13.custom.css',
               'css/jquery.jcrop.css',
               'css/jquery.fileupload-ui.css',
               'css/grid.css',
               'css/common.css',
               'css/afisha.css',
               'css/blog.css',
               'css/banners.css',
               'css/icons.css',
               'css/rating.css',
               'css/slider.css'
              ),
        filters='cssmin',
        output='cache/packed.css')

#CSS
register('light_css',
        Bundle('css/common.css',
              ),
        filters='cssmin',
        output='cache/light.css')

