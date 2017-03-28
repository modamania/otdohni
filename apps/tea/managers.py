from django.db import models

class InterviewManager(models.Manager):
    """Manager for Interview model"""

    def live(self):
        """Returns active interviews"""

        return self.filter(is_published=True)

    def without_last(self):
        """ Returns all active interviews without last"""

        queryset = self.live().order_by('pub_date')[1:]

        return queryset.reverse()
