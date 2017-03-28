from django import forms
from tinymce import widgets as tinymce_widgets

from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


class LocalFlatPageForm(FlatpageForm):
    content = forms.CharField(widget=tinymce_widgets.TinyMCE)

class LocalFlatPageAdmin(FlatPageAdmin):
    form = LocalFlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, LocalFlatPageAdmin)
