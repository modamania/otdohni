from django import forms
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from ajax_validation.utils import LazyEncoder
from ajax_validation.importpath import importpath


AJAX_FORMS = getattr(settings, 'AJAX_VALIDATION_FORMS', [])

def get_form_class(form_name):
    """
    Get form_class by form_name.

    Return None specified form_name exists and form_path not in settings.AJAX_FORMS is None.

    """
    for check in [importpath(form_path)
            for form_path in AJAX_FORMS]:
        if form_name.lower() == check.__name__.lower():
            form_class = check
            break
    else:
        form_class = None

    return form_class


@csrf_exempt
def validate(request, form_name, *args, **kwargs):
    form_class = get_form_class(form_name)
    extra_args_func = kwargs.pop('callback', lambda request, *args, **kwargs: {})
    kwargs = extra_args_func(request, *args, **kwargs)
    kwargs['data'] = request.POST
    form = form_class(**kwargs)
    if form.is_valid():
        data = {
            'valid': True,
        }
    else:
        if request.POST.getlist('fields'):
            fields = request.POST.getlist('fields') + ['__all__']
            errors = dict([(key, val) for key, val in form.errors.iteritems() if key in fields])
        else:
            errors = form.errors
        final_errors = {}
        for key, val in errors.iteritems():
            if key == '__all__':
                final_errors['__all__'] = val
            else:
                if not isinstance(form.fields[key], forms.FileField):
                    html_id = form.fields[key].widget.attrs.get('id') or form[key].auto_id
                    html_id = form.fields[key].widget.id_for_label(html_id)
                    final_errors[html_id] = val
        data = {
            'valid': False,
            'errors': final_errors,
        }
    json_serializer = LazyEncoder()
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')
validate = require_POST(validate)
