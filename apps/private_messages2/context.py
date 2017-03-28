from models import Chain


def count_unread_message(request):
    if request.user.is_authenticated():
        count = Chain.objects.get_count_unread(request.user)
    else:
        count = None
    return {
        'COUNT_UNREAD_MESSAGE': count,
    }
