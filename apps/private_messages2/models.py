import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from managers import ChainManager

import datetime


class Chain(models.Model):
    members = models.ManyToManyField(User,
                        related_name='messages_chain',
                        blank=True, null=True)
    have_read = models.ManyToManyField(User,
                        blank=True, null=True)
    removed = models.ManyToManyField(User,
                        related_name='messages_chain_removed',
                        blank=True, null=True)
    last_modifed = models.DateTimeField(default=datetime.datetime.now)
    objects = ChainManager()


    class Meta:
        ordering = ['-last_modifed', '-id',]

    @property
    def last_message(self):
        try:
            return self.messages.order_by('-sent_at', '-id').all()[0]
        except KeyError:
            return self.messages.none()

    @property
    def first_message(self):
        return self.messages.order_by('sent_at', 'id').all()[0]

    def get_other_users(self, user):
        return self.members.exclude(pk=user.pk)

    def make_as_unread_by_user(self, user):
        self.have_read.remove(user)

    def make_as_read(self, user):
        self.have_read.add(user)

    def make_as_delete(self, user):
        self.removed.add(user)


class Message(models.Model):
    sender = models.ForeignKey(User,
                        related_name='messages_sent',
                        blank=True, null=True)
    chain = models.ForeignKey(Chain,
                        related_name='messages',
                        blank=True, null=True)
    body = models.TextField(_(u"Body"))
    sent_at = models.DateTimeField(_(u"sent at"),
                        default=datetime.datetime.now)

    class Meta:
        ordering = ['-sent_at', '-id',]