import datetime
import time
import os

from django.db import models
from django.contrib.comments.signals import comment_was_posted
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


from apps.common.models import ObjectSubscribe
from core.utils import md5, denormalize_comments
from threadedcomments.models import ThreadedComment


def gen_file_name(instance, filename):
    ext_filename = filename.split('.')[1]
    filename = filename.encode('ascii', 'ignore')
    if ext_filename == 'jpeg':
        ext_filename = 'jpg'
    filename = str(int(time.time())) + '_' + md5(filename + str(datetime.datetime.now())) + '.' + ext_filename
    return os.path.join('logo',  filename.lower() )


def comment_notification(sender, **kwargs):
    comment = kwargs['comment']
    if hasattr(comment.content_object, 'title'):
        title = comment.content_object.title
    else:
        title = comment.content_object.__unicode__()
    subject = 'New Comment on %s' % title

    subscribed_users = ObjectSubscribe.objects.filter(object_pk = comment.content_object.id)
    recipients = [s.user.email for s in subscribed_users] + list(settings.CONTENT_MANAGER_MAIL_LIST)
    message = 'Author: %s\n \nComment:\n%s' % (comment.user_name, comment.comment)
    message = render_to_string('notification/comment_notification_email.txt', { 'comment': comment })
    for r in recipients:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [r,])

comment_was_posted.connect(comment_notification)


def denormalize_comments_signal(sender, instance, created=False, **kwargs):
    denormalize_comments(instance.content_object)

models.signals.post_save.connect(denormalize_comments_signal,
                                    sender=ThreadedComment)
models.signals.post_delete.connect(denormalize_comments_signal,
                                    sender=ThreadedComment)


class ImagesByDate(models.Model):
    from_dt = models.DateField(_('Start date'))
    to_dt = models.DateField(_('End date'))
    picture = models.ImageField('Picture', upload_to=gen_file_name)

    class Meta:
        ordering = ('from_dt', 'to_dt')
        abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.from_dt, self.to_dt)


class Logo(ImagesByDate):
    def clean(self):
        if self.from_dt and self.to_dt:
            if self.from_dt > self.to_dt:
                raise ValidationError(_(u'The from_dt later of the to_dt '))
            l = Logo.objects.filter(from_dt__lte=self.to_dt, to_dt__gte=self.from_dt)
            if self.id:
                l = l.exclude(id=self.id)
            if l:
                raise ValidationError(_(u'Overlapping dates'))


class Wolf(ImagesByDate):
    def clean(self):
        if self.from_dt and self.to_dt:
            if self.from_dt > self.to_dt:
                raise ValidationError(_(u'The from_dt later of the to_dt '))
            l = Wolf.objects.filter(from_dt__lte=self.to_dt, to_dt__gte=self.from_dt)
            if self.id:
                l = l.exclude(id=self.id)
            if l:
                raise ValidationError(_(u'Overlapping dates'))