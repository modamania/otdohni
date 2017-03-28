from django import template
from contacts.forms import ContactForm


register = template.Library()


@register.inclusion_tag('contacts/tags/contact_form.html', takes_context=True)
def show_contact_form(context):
    """Return contact form"""
    return {
        'template': template,
        'form': ContactForm(),
    }
