"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    fixtures = ['auth.json']
    #urls = 'profile.urls'

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_show_profile(self):

        response = self.client.get(reverse('profile.views.profile_show', \
            args=[1]))
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get(reverse('profile.views.profile_show', \
            args=[404]))
        self.failUnlessEqual(response.status_code, 404)

        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.failUnlessEqual(user1.profile.can_edit(user1), True)
        self.failUnlessEqual(user1.profile.can_edit(user2), False)

