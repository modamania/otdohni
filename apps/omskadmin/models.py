from django.db import models
from django.contrib.auth.models import User

from common.models import WithSite


class SitesAdmin(User, WithSite):

    class Meta:
        proxy = True
