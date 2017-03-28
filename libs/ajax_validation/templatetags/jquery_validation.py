import os

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import get_template

import ajax_validation
from ajax_validation.views import get_form_class

register = template.Library()

VALIDATION_SCRIPT = open(os.path.join(os.path.dirname(ajax_validation.__file__), 'media', 'ajax_validation', 'js', 'jquery-ajax-validation.js')).read()

def include_validation():
    return '''<script type="text/javascript">%s</script>''' % VALIDATION_SCRIPT


class UrlsNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        try:
            form = template.resolve_variable(self.var_name, context)
        except template.VariableDoesNotExist:
            return ''
        form_name = form.__class__.__name__.lower()

        #true if form in settings.AJAX_FORMS
        if get_form_class(form_name):
            url = reverse('form_validate', args=[form_name])
            context['url'] = url
            t = get_template('ajax_validation/ajax_validation.html')
            c = context
            return t.render(c)
        else:
            return ''

@register.tag('ajax_validate')
def get_form(parser, token):
    tokens = token.contents.split()
    tag_name = tokens[0]
    if len(tokens) != 2:
        raise template.TemplateSyntaxError, '%r tag requires 2 arguments' % tag_name
    return UrlsNode(var_name=tokens[1])


register.simple_tag(include_validation)
