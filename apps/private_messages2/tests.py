# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from private_messages2.models import Chain


class TestMessagesMixing(TestCase):
    def setUp(self):
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')
        self.user3 = User.objects.get(username='user3')

        self.client1 = Client()
        self.client1.login(username='user1', password='pass')
        self.client2 = Client()
        self.client2.login(username='user2', password='pass')
        self.client3 = Client()
        self.client3.login(username='user3', password='pass')

    def check_inbox(self, client, count):
        response = client.get(reverse('messages_inbox'))
        self.assertEqual(len(response.context['chain_list']), count)

    def chech_unread(self, user, count):
        self.assertEqual(Chain.objects.get_count_unread(user), count)


class PostNewMessage(TestMessagesMixing):
    fixtures = ['auth']

    def test(self):
        data = {
            'recipient': 'user2,user3',
            'subject': 'message1_subject',
            'body': 'message1_body'
        }
        self.client1.post(reverse('messages_compose'), data)

        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 1)
        self.check_inbox(self.client3, 1)


class CheckView(TestMessagesMixing):
    fixtures = ['auth', 'messages']

    def test(self):
        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 1)
        self.check_inbox(self.client3, 1)
        # self.chech_unread(self.user1, 2)
        # self.chech_unread(self.user2, 2)
        # self.chech_unread(self.user3, 2)

        response = self.client2.get(reverse('messages_inbox'))
        chain = response.context['chain_list'][0]
        self.assertEqual(chain[1], False)
        response = self.client2.get(reverse('messages_view', args=[chain[0].pk]))
        self.assertEqual(response.context['chain'], chain[0])

        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 1)
        self.check_inbox(self.client3, 1)
        # self.chech_unread(self.user1, 2)
        # self.chech_unread(self.user2, 1)
        # self.chech_unread(self.user3, 2)


class AnswerMessage(TestMessagesMixing):
    fixtures = ['auth', 'messages']

    def test(self):
        response = self.client2.get(reverse('messages_inbox'))
        chain = response.context['chain_list'][0][0]
        data = {
            'sender' : self.user2.pk,
            'chain' : chain.pk,
            'body' : 'message2_body',
        }
        response = self.client2.post(reverse('messages_view', args=[chain.pk]), data)
        self.assertEqual(response.status_code, 302)
        last_message = chain.last_message
        self.assertEqual(last_message.body, 'message2_body')


class CheckDelete(TestMessagesMixing):
    fixtures = ['auth', 'messages']

    def test(self):
        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 1)
        self.check_inbox(self.client3, 1)

        response = self.client2.get(reverse('messages_inbox'))
        chain = response.context['chain_list'][0][0]

        response = self.client2.get(reverse('messages_delete', args=[chain.pk]))
        self.assertEqual(response.status_code, 302)

        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 0)
        self.check_inbox(self.client3, 1)

        response = self.client2.get(reverse('messages_undelete'))
        self.assertEqual(response.status_code, 302)

        self.check_inbox(self.client1, 1)
        self.check_inbox(self.client2, 1)
        self.check_inbox(self.client3, 1)