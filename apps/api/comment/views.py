from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType

from api.utils import json
from threadedcomments.models import ThreadedComment, RelatedComment

def relate_comment(request, acrion, comment_pk):
    if not request.user.is_authenticated():
        return HttpResponse(status=403)
    if not acrion in ('remove_vote', 'agree', 'disagree'):
        raise Http404
    comment = get_object_or_404(ThreadedComment, pk=comment_pk)
    if acrion == 'remove_vote':
        RelatedComment.objects.filter(user=request.user, comment=comment).delete()
    else:
        relate = RelatedComment.objects.get_or_create(comment=comment, user=request.user)[0]
        if acrion == 'agree':
            relate.relate = '+'
        else:
            relate.relate = '-'
        try:
            relate.save()
        except IntegrityError:
            pass
    return HttpResponse(status=200)

def remove_comment(request, comment_pk):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    comment = get_object_or_404(ThreadedComment, pk=comment_pk)
    comment.is_removed = True
    comment.save()
    obj = comment.content_object
    return redirect(obj.get_absolute_url())
