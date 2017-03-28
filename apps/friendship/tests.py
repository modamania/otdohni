from django_webtest import WebTest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from models import Friendship

def remove_friendship_if_present(user1, user2):
    try:
        friendship = user1.friends.get(to_user=user2)
    except ObjectDoesNotExist:
        pass
    else:
         friendship.delete()
    try:
        friendship = user2.friends.get(to_user=user1)
    except ObjectDoesNotExist:
        pass
    else:
        friendship.delete()


class OfferFriendshipAndWithdraw(WebTest):
    fixtures = ['auth.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        remove_friendship_if_present(self.user1, self.user2)

    def test(self):
        user1 = self.user1
        user2 = self.user2
        link = reverse('friendship.views.add_friendship', args=[user2.pk])
        page = self.app.get(link, extra_environ=dict(REMOTE_USER='user1'))
        link = reverse('friendship.views.remove_friendship', args=[user2.pk])
        page = self.app.get(link, extra_environ=dict(REMOTE_USER='user1'))

    def tearDown(self):
        remove_friendship_if_present(self.user1, self.user2)

class OfferFriendshipAndConfirm(WebTest):
    fixtures = ['auth.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        remove_friendship_if_present(self.user1, self.user2)

    def test(self):
        user1 = self.user1
        user2 = self.user2
        link = reverse('friendship.views.add_friendship', args=[user2.pk])
        page = self.app.get(link, extra_environ=dict(REMOTE_USER='user1'))
        link = reverse('friendship.views.add_friendship', args=[user1.pk])
        page = self.app.get(link, extra_environ=dict(REMOTE_USER='user2'))

    def tearDown(self):
        remove_friendship_if_present(self.user1, self.user2)

class RemoveFriendship(WebTest):
    fixtures = ['auth.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        friendship = Friendship(from_user=self.user1, to_user=self.user2)
        friendship.save()

    def test(self):
        user1 = self.user1
        user2 = self.user2
        link = reverse('friendship.views.remove_friendship', args=[user2.pk])
        page = self.app.get(link, extra_environ=dict(REMOTE_USER='user1'))

    def tearDown(self):
        remove_friendship_if_present(self.user1, self.user2)
