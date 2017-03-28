from apps.sorl.thumbnail.main import DjangoThumbnail
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import os

try:
    def thumbnail(image_path):
        t = DjangoThumbnail(relative_source=image_path, requested_size=(100,100))
        return u'<img src="%s" alt="%s" />' % (t.absolute_url, image_path)
except ImportError:
    def thumbnail(image_path):
        absolute_url = os.path.join(settings.MEDIA_ROOT, image_path)
        return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)

class ImageWidget(forms.FileInput):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name and file_name != 'None':
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s" class="fancybox">%s</a><br />%s: ' %\
                              (file_path, thumbnail(file_name), _('Change')))
            except IOError: # not image
                output.append('%s: <a target="_blank" href="%s">%s</a> <br />%s: ' %\
                              (_('Currently'), file_path, file_name, _('Change')))

        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
