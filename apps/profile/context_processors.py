#-*- coding: utf-8 -*-

from django.conf import settings

def online_users(request):
    try:
        online_auth_users = request.online_users[0]
        online_anonymous_users = request.online_users[1]
    except:
        online_auth_users = 0
        online_anonymous_users = 0
    return {
        'online_auth_users': online_auth_users,
        'online_anonymous_users': online_anonymous_users,
    }

