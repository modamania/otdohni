from django.contrib.sites.models import Site

def sites_context(request):
    current_site = Site.objects.get_current()
    other_site = Site.objects.exclude(id=current_site.id)
    return {
        "current_site": current_site,
        "other_site": other_site,
    }
