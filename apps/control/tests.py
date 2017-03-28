# -*- coding: utf-8 -*-
import re
from django.core import mail
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission
 
class ControlTest(WebTest):
    fixtures = ['auth.json']
 
    def test_access_to_dashboard(self): 
        link_for_test = reverse('control.views.dashboard')
#access superuser
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user1'))
        self.assertEqual(page.status_int, 200)

#access user without access_to_dasboard
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=403)
        self.assertEqual(page.status_int, 403)

#access user with access_to_dasboard
        user2 = User.objects.get(pk=2)
        user2.profile.access_to_dasboard = True
        user2.profile.save()
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'))
        self.assertEqual(page.status_int, 200)

#remove access_to_dasboard
        user2.profile.access_to_dasboard = False
        user2.profile.save()

    def test_access_to_user_list(self): 
        link_for_test = reverse('control.views.user_list')
#access superuser
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user1'))
        self.assertEqual(page.status_int, 200)

#access user without access_to_dasboard and without permission to auth
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=403)
        self.assertEqual(page.status_int, 403)

#access user with access_to_dasboard and without permission to auth
        user2 = User.objects.get(pk=2)
        user2.profile.access_to_dasboard = True
        user2.profile.save()
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=403)
        self.assertEqual(page.status_int, 403)

#access user with access_to_dasboard and with permission to auth
        perm_change_user = Permission.objects.get(codename='change_user')
        user2.user_permissions.add(perm_change_user)
        user2.save()
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=200)
        self.assertEqual(page.status_int, 200)

#remove access_to_dasboard and permission to auth
        user2.profile.access_to_dasboard = False
        user2.profile.save()
        user2.user_permissions.remove(perm_change_user)
        user2.save()

    def test_access_to_user_edit(self):
        link_for_test = reverse('control.views.user_edit', args=[2])
#access superuser
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user1'))
        self.assertEqual(page.status_int, 200)

#access user without access_to_dasboard and without permission to auth
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=403)
        self.assertEqual(page.status_int, 403)

#access user with access_to_dasboard and without permission to auth
        user2 = User.objects.get(pk=2)
        user2.profile.access_to_dasboard = True
        user2.profile.save()
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=403)
        self.assertEqual(page.status_int, 403)

#access user with access_to_dasboard and with permission to auth
        perm_change_user = Permission.objects.get(codename='change_user')
        user2.user_permissions.add(perm_change_user)
        user2.save()
        page = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user2'), status=200)
        self.assertEqual(page.status_int, 200)

#remove access_to_dasboard and permission to auth
        user2.profile.access_to_dasboard = False
        user2.profile.save()
        user2.user_permissions.remove(perm_change_user)
        user2.save()

#commit form
        form = self.app.get(link_for_test, extra_environ= \
            dict(REMOTE_USER='user1')).form
        response = form.submit()
        self.assertEqual(response.status_int, 302)

