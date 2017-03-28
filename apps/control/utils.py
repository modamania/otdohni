from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs

from functools import wraps

from PIL import Image


def can_access():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated() and user.profile.access_to_dasboard:
                return view_func(request, *args, **kwargs)
            if user.is_authenticated() and user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wraps(view_func, assigned=available_attrs(view_func)) \
            (_wrapped_view)
    return decorator

def crop_image(image, x, y, w, h):
    im = Image.open(image.file)
    size_percent = map(lambda x: x/100, im.size)
    box = map(lambda x: int(round(x)), (
        x*size_percent[0],
        y*size_percent[1],
        (x+w)*size_percent[0],
        (y+h)*size_percent[1],
    ))
    im = im.crop(box)
    im.save(image.file.name)
    image.generate_thumbnails();
