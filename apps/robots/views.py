from apps.robots.models import RobotsItem
from django.shortcuts import render_to_response, get_object_or_404

def robots(request):
    template = 'robots/robots.html'
    robots_text = get_object_or_404(RobotsItem, url=request.META['HTTP_HOST']).content
    context = {'robots_text': robots_text}

    return render_to_response(template, context,
        mimetype='text/plain')

