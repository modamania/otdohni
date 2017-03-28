from django.db import models
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from settings import DEFAULT_FROM_EMAIL


class FriendshipManager(models.Manager):
    def friendship_exists(self, fr, to):
        # fr == from )
        return self.friendship_filter(fr, to).exists()

    def friendship_delete(self, fr, to):
        return self.friendship_filter(fr, to).delete()

    def friendship_create(self, fr, to):
        if self.friendship_exists(fr, to):
            return self.filter(
                models.Q(
                    from_user=fr,
                    to_user=to,
                ) |
                models.Q(
                    from_user=to,
                    to_user=fr,
                )
            ).update(is_confirm=True)
        else:
            d = {
                'nick':fr.username,
                'name': fr.first_name,
                'friend_url': reverse('profile_show', args=[fr.pk]),
                'current_domain': Site.objects.get_current().domain,
                }
            subject = _('%(nick)s (%(name)s) wants to be friends with you.') % d
            content = _('%(nick)s (%(name)s) wants to be friends with you and waiting for your approval. Accept or reject the request.\n\n%(nick)s (%(name)s) Profile: http://%(current_domain)s%(friend_url)s \n\nPlease note: This letter was automatically sent from the site http://%(current_domain)s.') %  d

            from_email, to_email = DEFAULT_FROM_EMAIL, to.email
            send_mail(subject, content, from_email, [to_email])

            return self.create(from_user=fr, to_user=to)

    def friendship_filter(self, fr, to):
        return self.filter(
            models.Q(
                from_user=fr,
                to_user=to,
            ) |
            models.Q(
                from_user=to,
                to_user=fr,
            )
        )
