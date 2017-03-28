from django.contrib.sites.models import Site
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q

class ActionManager(models.Manager):
    """ Action model manager """

    def published(self):
        """ Returns all published actions"""
        return self.filter(is_published=True, sites = Site.objects.get_current())

    def current(self):
        """ Returns all current (not completed) actions"""
        return self.published().filter(is_completed=False).order_by('-pub_date')

    def completed(self):
        """ Returns all closed actions"""
        return self.published().filter(is_completed=True).order_by('-pub_date')


class PollManager(models.Manager):
    """ Poll model manager """

    def published(self):
        """ Returns all published actions"""
        return self.filter(is_published=True)

    def soon(self):
        return self.published().filter(status='SOON')

    def current(self):
        return self.published().filter(Q(status='ACTIVE') | Q(status='NONE'))

    def completed(self):
        return self.published().filter(status='COMPLETED')

    def suspend(self):
        return self.published().filter(status='SUSPEND')

    def add_like(self, user, work):
        #if user.is_authenticated() and user not in work.user_likes.all():
        #    work.user_likes.add(user)
        work.total_likes += 1
        work.save()
        return True

