from django.db import models


class ChainManager(models.Manager):
    def inbox(self, user):
        return user.messages_chain.exclude(removed__pk=user.pk) \
            .prefetch_related('members', 'members__profile', 'have_read', 'messages')

    def get_chain_for_messages(self, mid_list):
        return self.filter(messages__id__in=mid_list).distinct()

    def get_count_unread(self, user):
        return user.messages_chain.exclude(have_read__pk=user.pk).exclude(removed__pk=user.pk).count()

    def get_chain_count(self, mid_list):
        return self.get_chain_for_messages(mid_list).count()
