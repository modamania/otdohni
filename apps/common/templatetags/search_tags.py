from django import template

register = template.Library()


TEXT_FIELDS = {
    'groups.group': 'description',
    'traveloptions.trip': 'short_description',
    'events.event': 'description',
    'profiles.profile': 'about',
    'traveloptions.destination': 'short_description',
    'travellogs2.travel': 'introduction',
}

def _set_text(obj):
    if hasattr(obj, 'text'):
        return
    app = obj._meta.app_label
    model = obj._meta.module_name
    key = '%s.%s' % (app, model)
    
    if key in TEXT_FIELDS:
        obj.text = getattr(obj, TEXT_FIELDS[key])
        


@register.simple_tag
def search_result(search_result, search_type):
    "Returns template by search type"
    result = search_result.object
    _set_text(result)
    
    if search_type:
        app = result._meta.app_label
        model = result._meta.module_name
        template_name = "search/results/{0}_{1}.html".format(app, model)
    else:
        template_name = 'search/results/_all.html'

    context = {
        'object': result,
        'result_type': result._meta.verbose_name_plural
    }
    try:
        return template.loader.render_to_string(template_name, context)
    except template.TemplateDoesNotExist:
        return template.loader.render_to_string("search/results/default.html", context)
