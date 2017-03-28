"""
Change the attributes you want to customize
"""
from django.core import urlresolvers

from threadedcomments.models import ThreadedComment
from threadedcomments.forms import ThreadedCommentForm

def get_model():
    return ThreadedComment

def get_form():
    return ThreadedCommentForm

def get_form_target():
    return urlresolvers.reverse("threadedcomments.views.post_comment")

from django.utils.translation import ugettext_lazy as _
_('Threadedcomments')
