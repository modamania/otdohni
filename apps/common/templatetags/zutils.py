from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def sub_domain(context):
	return context['current_site'].domain.split('.')[0]