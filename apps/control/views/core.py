from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import SortedDict
from django import forms
from django.shortcuts import redirect, get_object_or_404

from control.utils import can_access
from control.widgets import ImageWidget
from annoying.decorators import render_to

from apps.core import models


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        for k,f in self.fields.items():
            if type(f) == forms.fields.DateField:
                self.fields[k].widget = forms.TextInput(attrs={'class':'datepicker'})
            if type(f) == forms.ImageField:
                self.fields[k].widget = ImageWidget()

def create_form(model):
    meta = type('Meta', (), { "model":model, })
    modelform_class = type('modelform', (MyModelForm,), {"Meta": meta})
    return modelform_class

@can_access()
@render_to('control/core/dashboard.html')
def dashboard(request):
    return {}


@can_access()
@render_to('control/core/list.html')
def list(request, model_name):
    CLS = ContentType.objects.get(app_label="core", model=model_name).model_class()
    fields = CLS._meta.fields
    data = SortedDict()
    for item in CLS.objects.all():
        data[item.id] = tuple(getattr(item, f.name) for f in fields)
    return {
        'fields': fields,
        'meta' : CLS._meta,
        'list': data,
    }


@can_access()
@render_to('control/core/form.html')
def form(request, model_name, pk=None):
    CLS = ContentType.objects.get(app_label="core", model=model_name).model_class()
    modelform_class = create_form(CLS)

    if pk:
        instance = get_object_or_404(CLS, pk=pk)
    else:
        instance = None
    form = modelform_class(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/'.join(('','control','core',model_name,'')))

    return {
        'meta' : CLS._meta,
        'form' : form,
    }


@can_access()
def remove(request, model_name, pk):
    CLS = ContentType.objects.get(app_label="core", model=model_name).model_class()
    modelform_class = create_form(CLS)
    CLS.objects.get(pk=pk).delete()
    return redirect('/'.join(('','control','core',model_name,'')))
