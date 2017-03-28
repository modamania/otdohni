# -*- coding: utf-8 -*-
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from os.path import join as os_path_join
from datetime import datetime
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _

from settings import *
from core.utils import md5


SEX_CHOICES = (
    ('none', _('none')),
    ('male', _('male')),
    ('female', _('female')),
)

def gen_file_name(instance, filename):
    ext_filename = filename.split('.')[1]
    filename = filename.encode('ascii', 'ignore')
    if ext_filename == 'jpeg':
        ext_filename = 'jpg'
    filename = str(instance.pk) + '_' + md5(filename + str(datetime.now())) + '.' + ext_filename
    return os_path_join('userpic',  filename.lower() )


class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, related_name="profile")
    userpic = ImageWithThumbnailsField(upload_to=gen_file_name,\
        thumbnail={'size': (120, 120), 'options': {'crop':'center'}, 'quality': (100), 'subdir': 'large'}, \
        extra_thumbnails = {
            'medium': {'size': (60, 60), 'options': {'crop':',0'}, 'quality': (100), 'subdir': 'medium'},
            'small': {'size': (24, 24), 'options': {'crop':',10'}, 'quality': (100), 'subdir': 'small'},
        },\
        null=True, blank=True)
    sex = models.CharField(max_length=6,
                        choices=SEX_CHOICES, default='none')
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50,
                        null=True, blank=True)
    city = models.CharField(max_length=50,
                        null=True, blank=True)
    web_site = models.URLField(verify_exists=False,
                        null=True, blank=True)
    icq = models.CharField(max_length=15, null=True, blank=True)
    profession = models.TextField(null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50,
                        null=True, blank=True)
    interest = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    access_to_dasboard = models.BooleanField(default=False)
    subscription_accepted = models.BooleanField(default=True)
    subscribed = models.BooleanField(default=False)

    """
    class Meta:
        permissions = (('dashboard_access'),_('Can login to control panel'))
    """ #TODO: Discuss this

    def __unicode__(self):
        if self.user.first_name and self.user.last_name:
            return u"%s %s" % (self.user.first_name , self.user.last_name)

        if self.user.first_name:
            return self.user.first_name

        if self.user.last_name:
            return self.user.last_name

        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_show', args=[self.user.id])

    def can_edit(self, user):
        return self.user == user

    def get_userpic(self):
        if os.path.isfile(self.userpic.path):
            return "/media/%s" % self.userpic
        return "/static/i/no_avatar.png"

    @property
    def filled(self):
        return True

class OldAuth(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name="old_auth")
    password = models.CharField(max_length=32)
