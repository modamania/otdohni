from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def form_field(form, field_name):
    field = form[field_name]
    return render_to_string('common/form_field.html', {'f': field,})