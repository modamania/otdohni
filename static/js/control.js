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


function getId(classes) {
    var match = /.*elem_(\d+).*/.exec(classes);
    if (match) {
        return match[1];
    } else {
        return null;
    };
};

function getParentPhoto(elem) {
    return elem.parents('.gallery__photo_item');
}

function incInitialForms() {
    var initial = $('.photo_upload [name$=INITIAL_FORMS]')
    var val = parseInt(initial.val())
    initial.val(val+1)
}

function Photo(elem) {
    // base element
    this.elem = elem;

    // options
    this.delay = 200;

    // properties
    this.is_active = function() {
        if (this.elem.hasClass('elem_active')) {
            return true;
        };
        return false;
    };

    // private
    this._getPopup = function() {
        var id = getId(this.elem.attr('class'))
        return $('.popup_elem_' + id)
    };

    this.getFormId = function() {
        popup = this._getPopup()
        name = popup.find('[name$=title]').attr('name')
        return parseInt(/\d{1,2}/.exec(name)[0])
    };

    this._replaceNameAndId = function(elem, index) {
        var pattern = /\d{1,2}/
          , name = elem.attr('name')
          , id = elem.attr('id')

        elem.attr('name', name.replace(pattern, index));
        elem.attr('id', id.replace(pattern, index));
    };

    this._updateNum = function(index) {

        var popup = this._getPopup()
        var elems = [
            this.elem.find('[name$=order]'), 
            this.elem.find('[name$=place]'),
            this.elem.find('[name$=id]'),
            this.elem.find('[name$=DELETE]'),
            this.elem.find('[name$=crop_x]'),
            this.elem.find('[name$=crop_y]'),
            this.elem.find('[name$=crop_x2]'),
            this.elem.find('[name$=crop_y2]'),
            popup.find('[name$=title]'),
            popup.find('[name$=image]'),
        ];

        for (var i=0; i<elems.length; i++) {
            var elem = elems[i];
            this._replaceNameAndId(elem, index);
        };
    };

    this.getId = function() {
        return getId(this.elem.attr('class'));
    }

    this.setLegend = function(index) {
        this.elem.find('.legend').text(index);
    };

    this.setOrder = function(index) {
        this.elem.find('[name$=order]').val(index);
    };

    this.delete = function() {
        // move deleted elem to the #gellery__deleted_photots
        this.elem.find('[name$=DELETE]').attr('checked', true);
        this.elem.removeClass('elem_active');
        this.elem.appendTo($('#gallery__deleted_photos'));
        this.clearCoordinate();
    };

    this.clearCoordinate = function() {
        this.elem.find('.coordinate').val(undefined);
    };

    this.toggle = function() {
        if (this.css('display') == 'none') {
            this.elem.show(this.delay);
        } else {
            this.elem.hide(this.delay);
        }
    };

    this.togglePopup = function() {
        var popup = this._getPopup();
        if (popup.css('display') == 'none') {
            popup.show(this.delay);
            return true;
        };
        popup.hide(this.delay);
        return false
    };

    this.hidePopup = function() {
        var popup = this._getPopup();
        if (popup.css('display') != 'none') {
            popup.hide(this.delay);
        }
    };

    this.getData = function() {
        var order = this.elem.find('input[name$=order]').val()
          , gallery_id = this.elem.find(':hidden[name$=id]').val()

        return {
            'order': order,
            'gallery_id': gallery_id,
        }
    };

    this._activate = function() {
        this.elem.addClass('elem_active').removeClass('fieldset_empty');
        this.elem.find('.gallery__delete_photo').removeClass('hidden');
        this.elem.find(':file[name$=image]:first').remove();
    };

    this._deactivate = function() {
        this.elem.removeClass('elem_active').addClass('fieldset_empty');
        this.elem.find('.gallery__delete_photo').addClass('hidden');
        this.elem.find(':file[name$=image]:first').remove();
    };

    this.setDataNew = function(data) {
        var order = data['order']
          , image_url = data['image_url']
          , image_thumb_url = data['image_thumb_url']
          , gallery_id = data['gallery_id']
          , popup = this._getPopup()

        this.elem.find('input[name$=order]').val(order);
        this.elem.find(':hidden[name$=id]').val(gallery_id);
        this.elem.find('.photo__thumb').attr('src', image_thumb_url);
        popup.find('.gallery__photo').attr('src', image_url);

        if (this.is_active()) {
            this._deactivate()
        } else {
            this._activate();
            this.togglePopup()
        }
        this.jcropUpdate();
        return false
    };

    this.setDataChange = function(data) {
        var image_url = data['image_url']
          , image_thumb_url = data['image_thumb_url']
          , popup = this._getPopup()

        popup.find('.gallery__photo').attr('src', image_url);
        this.elem.find('.photo__thumb').attr('src', image_thumb_url);
        
        this.jcropUpdate();
        return false
    };

    this.hasJcrop = function() {
        if (this.jcrop_api) {
            return true
        }
        return false
    }

    this.setJcrop = function() {
        var popup = this._getPopup()
        var self = this
          , imag = popup.find('.gallery__photo')

        var crop_x = this.elem.find(':hidden[name$=crop_x]');
        var crop_y = this.elem.find(':hidden[name$=crop_y]');
        var crop_x2 = this.elem.find(':hidden[name$=crop_x2]');
        var crop_y2 = this.elem.find(':hidden[name$=crop_y2]');

        function save_index(c) {
            if (!(c.x == c.x2 && c.y == c.y2)) {
                crop_x.val(c.x/(imag[0].width/100));
                crop_y.val(c.y/(imag[0].height/100));
                crop_x2.val(c.w/(imag[0].width/100));
                crop_y2.val(c.h/(imag[0].height/100));
            } else {
                crop_x.val(undefined);
                crop_y.val(undefined);
                crop_x2.val(undefined);
                crop_y2.val(undefined);
            }
        }

        imag.each(function() {
                $(this).Jcrop({
                    onSelect: save_index,
                    onChange: save_index,
                }, function() { self.jcrop_api = this });
        });
    };

    this.jcropEnable = function() {
        if (!this.hasJcrop()) {
            this.setJcrop();
        }
        this.jcrop_api.enable();
    };

    this.jcropDisable = function() {
        if (!this.hasJcrop()) {
            this.setJcrop();
        };
        this.jcrop_api.disable();
    }

    this.jcropDestroy = function() {
        if (this.hasJcrop()) {
            this.jcrop_api.destroy();
        }
    };

    this.jcropUpdate = function() {
        if (this.hasJcrop()) {
            this.jcropDestroy();
        };
        this.setJcrop();
    };

    this.cancelNewPhoto = function() {
        var popup = this._getPopup()
        var image = this.elem.find('.photo__thumb')
          , thumb = popup.find('.photo__thumb')
          , id = this.getFormId()
        this._deactivate();

        image.attr('src', '');
        thumb.attr('src', '');
        this.togglePopup();
        var input = $("<input type='file' />").attr({
            'name': 'gallery-' + id + '-image',
            'id': 'id_gallery-' + id + '-image',
        })
        this.elem.append(input);
        return input
    };
}

function Gallery() {
    // private
    this._makePhotos = function() {
        var photos = []
        $('#gallery__photos .gallery__photo_item').each(function() {
            var elem = new Photo($(this));
            photos.push(elem);
        });
        return photos
    };

    this._makeDeletedPhotos = function() {
        var photos = []
        $('#gallery__deleted_photos .gallery__photo_item').each(function() {
            var elem = new Photo($(this));
            photos.push(elem);
        });
        return photos
    };

    this._wrappedPhotos = function() {
        var wrapped_photos = $()
        for (var i=0; i<this.photos.length; i++) {
            wrapped_photos = wrapped_photos.add(this.photos[i])
        }
        return wrapped_photos
    };

    // init
    this.photos = this._makePhotos();
    this.deleted_photos = [];

    this.getActivePhotos = function() {
        var active_photos = []
          , inactive_photos = []

        for (var i=0; i<this.photos.length; i++) {
            var elem = this.photos[i];
            if (elem.is_active()) {
                active_photos.push(elem);
            } else {
                inactive_photos.push(elem);
            }
        }
        this.inactive_photos = inactive_photos;
        this.active_photos = active_photos;
        return active_photos
    }

    this.getPhotoById = function(elem_id) {
        for (var i=0; i<this.photos.length; i++) {
            var current_elem = this.photos[i];
            var current_id = current_elem.getId();
            if (current_id == elem_id) {
                return current_elem
            }
        }
    }

    this.photosExclude = function() {
        this.photos = this._makePhotos();
    };

    this.cancelNewPhotoById = function(elem_id) {
        var elem = this.getPhotoById(elem_id)
        return elem.cancelNewPhoto()
    };

    this.deletePhoto = function(elem_id) {
        var elem = this.getPhotoById(elem_id);
        elem.delete();
        this.photosExclude();
        this.updateIndex();
        this._updateNumForms();
    };

    this.updateIndex = function() {
        // update legend
        this.photos = this._makePhotos();
        for (var i=0; i<this.photos.length; i++) {
            var elem = this.photos[i];
            elem.setLegend(i+1);
        };
        var active_photos = this.getActivePhotos();
        for (var i=0; i<active_photos.length; i++) {
            var elem = active_photos[i];
            elem.setOrder(i+1);
        };
    };

    this.createSortable = function() {
        var self = this
        // WTF ???
        function update() {
            self.photos = self._makePhotos();
            for (var i=0; i<self.photos.length; i++) {
                var elem = self.photos[i];
                elem.setLegend(i+1)
            }
            var active_photos = self.getActivePhotos()
            for (var i=0; i<active_photos.length; i++) {
                var elem = active_photos[i];
                elem.setOrder(i+1);
            }
        }
        $('#gallery__photos').sortable({
            items: $('.elem_active'),
            update: update
        });
    };

    this._disableSortable = function() {
        $('#gallery__photos').sortable('disable');
    };

    this._enableSortable = function() {
        $('#gallery__photos').sortable('enable');
    };

    this._refreshSortable = function() {
        $('#gallery__photos').sortable('refresh');
    };

    this._updateSortable = function() {
        $('#gallery__photos').sortable('destroy');
        this.createSortable();
    }

    this._hidePhotoPopup = function() {
        for (var i=0; i<this.photos.length; i++) {
            var elem = this.photos[i];
            elem.hidePopup();
        }
    };

    this._getNewOrder = function() {
        var active_photos = this.getActivePhotos();
        return active_photos.length + 1
    };

    this.togglePhotoPopup = function(elem_id) {
        var photo = this.getPhotoById(elem_id);
        $('.elem_' + elem_id + ' .photo_title').html($('#id_gallery-' + (elem_id-1) + '-title').val());
        this._hidePhotoPopup();
        if (photo.togglePopup()){
            this._disableSortable();
        } else {
            this._enableSortable();
        }
    }

    this.getDataById = function(elem_id) {
        var place_id = $('input[name=place_id]').val()
          , photo = this.getPhotoById(elem_id)

        var data = photo.getData()
        if (!data['order']) {
            data['order'] = this._getNewOrder();
        };
        data['place_id'] = place_id;
        return data
    };

    this.setDataByIdNew = function(elem_id, data) {
        var photo = this.getPhotoById(elem_id)
        var created = photo.setDataNew(data)

        if (created) {
            this._updateSortable();
            incInitialForms();
            this._updateNumForms();
        }
    };

    this.setDataByIdChange = function(elem_id, data) {
        var photo = this.getPhotoById(elem_id)
        var created = photo.setDataChange(data)
    };

    this.createPhotosJcrop = function() {
        for (var i=0; i<this.photos.length; i++) {
            var photo = this.photos[i];
            photo.setJcrop();
        }
    }

    this.getDeletedPhotos = function() {
        var deleted_photos = []
        $('#gallery__deleted_photos .gallery__photo_item').each(function() {
            var elem = new Photo($(this));
            deleted_photos.push(elem);
        });
        return deleted_photos
    }

    this.getAllInactivePhotos = function() {
        var all_inactive = []
        $('.gallery__photo_item').not('.elem_active').each(function() {
            var elem = new Photo($(this));
            all_inactive.push(elem);
        });
        return all_inactive
    }

    this._updateNumForms = function() {
        var active = this.getActivePhotos()
          , inactive = this.inactive_photos
          , deleted = this._makeDeletedPhotos()

        if (deleted.length) {
            active = active.concat(deleted);
        };
        if (inactive.length) {
            active = active.concat(inactive);
        };

        for (var i=0; i<active.length; i++) {
            var photo = active[i]
            photo._updateNum(i);
        };
    }
}


$(function() {

    // GALLERY INITIALIZE
    gallery = new Gallery();
    gallery.createSortable();
    gallery.createPhotosJcrop();

    var token = $('[name=csrfmiddlewaretoken]').val();

    $('.gallery__delete_photo i').click(function() {
        if (window.confirm("Вы действительно хотите удалить фотографию?")) {
            var elem_id = getId($(this).parents('.gallery__photo_item').attr('class'));
            if (elem_id) {
                gallery.deletePhoto(elem_id)
            }
        }
    });

    $('.photo__thumb').click(function() {
        var elem_id = getId($(this).parents('.gallery__photo_item').attr('class'));
        if (elem_id) {
            var data = gallery.getDataById(elem_id)
            gallery.togglePhotoPopup(elem_id)
            gallery.setDataByIdChange(elem_id, data)
        }
    });

    $('.upload__popup .submit').click(function() {
        var elem_id = getId(
            $(this).parents('.upload__popup').attr('class'))
        if (elem_id) {
            gallery.togglePhotoPopup(elem_id);
        }
        return false
    });

    function ChangeFilePreview() {
        var elem_id = getId(
            $(this).parents('.gallery__photo_item').attr('class'))
        data = gallery.getDataById(elem_id);
        data['csrfmiddlewaretoken'] = token;

        function send(data) {
            gallery.setDataByIdNew(elem_id, data)
        }

        $(this).upload('/control/place/edit/gallery/', data, send, 'json')
    }

    $('.gallery__photo_item :file').change(ChangeFilePreview);

    $('.change_file').click(function() {
        $(this).next().toggle()
    });

    function ChangeFileListener() {
        var elem_id = getId(
                $(this).parents('.upload__popup').attr('class'))
        var data = gallery.getDataById(elem_id)
          , input = this

        data['csrfmiddlewaretoken'] = token;
        var input = this

        function send(data) {
            gallery.setDataByIdChange(elem_id, data);

            var input_id = input.id
              , input_wr = $(input)
              , input_nm = input_wr.attr('name')

            input_wr.replaceWith($("<input type='file' />").attr({
                'name': input_nm,
                'id': input_id
            }).change(ChangeFileListener))
        }

        $(this).upload('/control/place/edit/image/', data, send, 'json');
    }

    $('.upload__popup :file').change(ChangeFileListener);

    $('.upload__popup .cancel').click(function() {
        var elem_id = getId(
            $(this).parents('.upload__popup').attr('class'))
        if (elem_id) {
            gallery.togglePhotoPopup(elem_id);
        }
        return false;
        /*
        var data = gallery.getDataById(elem_id)
        data['csrfmiddlewaretoken'] = token;
        data['cancel'] = true;

        function send(data) {
            if (data.hasOwnProperty('empty')) {
                input = gallery.cancelNewPhotoById(elem_id)
                input.change(ChangeFilePreview);
                gallery._updateNumForms();
            } else {
                gallery.setDataByIdChange(elem_id, data)
            }
        }

        $.post('/control/place/edit/image/', data, send, 'json');
        return false;
        */
    });
});

$(window).scroll(function(){    
    getscroll();
        
    var form = $('.form_place_edit'),
        toolbar = form.find('.control_toolbar'),
        offset = $('.pathway').offset(),
        width = form.width(),
        top = offset.top + 2*toolbar.outerHeight()/3;
        
        if (yScroll > top) {
            toolbar.addClass('toolbar_fixed').css('width',width +'px');
        } else {
            toolbar.removeClass('toolbar_fixed');
        }
});
