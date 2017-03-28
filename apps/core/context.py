import datetime

from django.conf import settings
from django.contrib.sites.models import Site

from core.models import Logo, Wolf


def request_path(request):
    return {'REQUEST_PATH': request.path_info }

def media_url(request):
    my_media_url = settings.MEDIA_URL
    if not my_media_url.endswith('/'):
        my_media_url += '/'
    return {'MEDIA_URL': my_media_url}

def count_unread_message(request):
    if not request.user.is_anonymous():
        count = request.user.received_messages.filter(read_at__isnull=True, recipient_deleted_at__isnull=True,).count()
    else:
        count = None
    return {'COUNT_UNREAD_MESSAGE': count}

def sites(request):
    current_site = Site.objects.get_current()
    other_site = Site.objects.order_by('name')
    return {
        "current_site": current_site,
        "other_site": other_site,
        "CITY": current_site.city,
    }

def logo_and_wolf(request):
    today = datetime.date.today()
    try:
        cur_logo = Logo.objects.filter(from_dt__lte=today, to_dt__gte=today)[0]
    except IndexError:
        cur_logo = None
    try:
        cur_wolf = Wolf.objects.filter(from_dt__lte=today, to_dt__gte=today)[0]
    except IndexError:
        cur_wolf = None
    return {
        "cur_logo" : cur_logo,
        "cur_wolf" : cur_wolf,
    }