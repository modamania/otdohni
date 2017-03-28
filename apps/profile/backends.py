from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend as OrignModelBackend
from django.core.exceptions import ObjectDoesNotExist

from core.utils import md5
from profile.models import OldAuth

class OldAuth(OrignModelBackend):

    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """
    def authenticate(self, username=None, password=None):
        user = None
        try:
            check_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        try:
            if check_user.old_auth.password == md5(password):
                user = check_user
                user.set_password(password)
                user.save()
                user.old_auth.delete()
        except ObjectDoesNotExist:
            if check_user.check_password(password):
                user = check_user

        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
