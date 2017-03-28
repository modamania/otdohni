from django.db import models
from django.contrib.auth.models import User

from friendship.managers import FriendshipManager


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friends')
    to_user = models.ForeignKey(User, related_name='friend_to')
    is_confirm = models.BooleanField(default=False)

    objects = FriendshipManager()

    class Meta:
        unique_together = ('from_user', 'to_user')

    def is_friend(self, user):
        return self.objects.are_friends(self.from_user, user)
